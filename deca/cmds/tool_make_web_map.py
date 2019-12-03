from deca.vfs_db import vfs_structure_open
from deca.ff_avtx import Ddsc
from deca.ff_rtpc import Rtpc, PropName, RtpcProperty, RtpcNode
from deca.file import ArchiveFile
from deca.ff_types import *
from deca.ff_adf import adf_node_read
from deca.ff_adf_amf import AABB
from deca.ff_adf_amf_gltf import Deca3dMatrix
from deca.digest import process_translation_adf
from PIL import Image
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import shutil
import re


dst_x0 = 128
dst_y0 = -128
src_to_dst_x_scale = 128 / (16 * 1024)  # 180.0/(16*1024)
src_to_dst_y_scale = -128 / (16 * 1024)  # -90.0/(16*1024)


class RtpcLootVisitor:
    def __init__(self, tr):
        self.tr = tr
        self.regions = []
        self.points = {
            'CLootCrateSpawnPoint': [],
            'CLootCrateSpawnPointGroup': [],
            'CPlayerSpawnPoint': [],
            'CCollectable': [],
            'CBookMark': [],
            'CPOI': [],
            'CPOI.nest_marker_poi': [],
        }

    def process(self, rtpc):
        if PropName.CLASS_NAME.value in rtpc.prop_map:
            rtpc_class = rtpc.prop_map[PropName.CLASS_NAME.value].data.decode('utf-8')

            if rtpc_class in {'CLootCrateSpawnPoint', 'CLootCrateSpawnPointGroup', 'CBookMark', 'CPOI', 'CCollectable',
                              'CPlayerSpawnPoint'}:
                self.process_point(rtpc),
            elif rtpc_class == 'CRegion':
                self.process_CRegion(rtpc)

    def process_point(self, rtpc):
        rtpc_class = rtpc.prop_map[PropName.CLASS_NAME.value].data.decode('utf-8')
        ref_matrix = Deca3dMatrix(col_major=rtpc.prop_map[0x6ca6d4b9].data)
        x = ref_matrix.data[0, 3]
        y = ref_matrix.data[2, 3]
        coords = [
            x * src_to_dst_x_scale + dst_x0,
            y * src_to_dst_y_scale + dst_y0,
        ]

        obj = {
            'type': 'Feature',
            'properties': {
                'type': rtpc_class,
            },
            'geometry': {
                'type': 'Point',
                'coordinates': coords,
            },
        }

        comment = ''
        if PropName.CLASS_COMMENT in rtpc.prop_map:
            comment = rtpc.prop_map[PropName.CLASS_COMMENT].data.decode('utf-8')
            obj['properties']['comment'] = comment

        if PropName.INSTANCE_UID in rtpc.prop_map:
            obj_id = rtpc.prop_map[PropName.INSTANCE_UID].data
            obj['properties']['uid'] = obj_id
            obj['properties']['uid_str'] = '0x{:012X}'.format(obj_id)

        if PropName.CPOI_NAME in rtpc.prop_map:
            cpoi_name = rtpc.prop_map.get(PropName.CPOI_NAME, RtpcProperty()).data.decode('utf-8')
            cpoi_name_tr = self.tr.get(cpoi_name, cpoi_name)
            obj['properties']['poi_name'] = cpoi_name
            obj['properties']['poi_name_tr'] = cpoi_name_tr

        if PropName.CPOI_DESC in rtpc.prop_map:
            cpoi_desc = rtpc.prop_map.get(PropName.CPOI_DESC, RtpcProperty()).data.decode('utf-8')
            cpoi_desc_tr = self.tr.get(cpoi_desc, cpoi_desc)
            obj['properties']['poi_desc'] = cpoi_desc
            obj['properties']['poi_desc_tr'] = cpoi_desc_tr

        if PropName.BOOKMARK_NAME in rtpc.prop_map:
            bookmark_name = rtpc.prop_map[PropName.BOOKMARK_NAME].data.decode('utf-8')
            obj['properties']['bookmark_name'] = bookmark_name

        if 0x34beec18 in rtpc.prop_map:
            loot_class = rtpc.prop_map[0x34beec18].data.decode('utf-8')
            obj['properties']['loot_class'] = loot_class

        name = 'CPOI.{}'.format(comment)
        if name in self.points:
            self.points[name].append(obj)
        else:
            self.points[rtpc_class].append(obj)

    def process_CRegion(self, rtpc):
        obj_type = rtpc.prop_map[PropName.CLASS_NAME].data.decode('utf-8')
        obj_id = rtpc.prop_map.get(PropName.INSTANCE_UID, RtpcProperty()).data
        comment = rtpc.prop_map.get(PropName.CLASS_COMMENT, RtpcProperty()).data.decode('utf-8')

        ref_matrix = Deca3dMatrix(col_major=rtpc.prop_map[0x6ca6d4b9].data).data
        border = np.array(rtpc.prop_map[PropName.CREGION_BORDER].data).reshape((-1, 4)).transpose()
        border[3, :] = 1.0
        border = np.matmul(ref_matrix, border)
        border = border.transpose()

        coords = border * np.array([src_to_dst_x_scale, 0, src_to_dst_y_scale, 0]) + np.array([dst_x0, 0, dst_y0, 0])
        coords = [list(v) for v in coords[:, [0, 2]]]

        obj = {
            'type': 'Feature',
            'properties': {
                'type': obj_type,
                'uid': obj_id,
                'uid_str': '0x{:012X}'.format(obj_id),
                'comment': comment,
            },
            'geometry': {
                'type': 'Polygon',
                'coordinates': [coords]
            },
        }
        self.regions.append(obj)


class ToolMakeWebMap:
    def __init__(self, vfs_config):
        if isinstance(vfs_config, str):
            self.vfs = vfs_structure_open(vfs_config)
        else:
            self.vfs = vfs_config

    def tileset_make(self, img, tile_path, tile_size=256, max_zoom=-1):
        # save full image, mainly for debugging
        os.makedirs(tile_path, exist_ok=True)
        img.save(os.path.join(tile_path, 'full.png'))

        # determine zoom levels
        sz = img.size
        max_width = max(*sz)
        zooms = 0
        w = tile_size
        while w <= max_width:
            zooms = zooms + 1
            w = w * 2

        # save tiles
        zimgs = [None] * zooms
        zimgs[-1] = img
        for z in range(zooms):
            zlevel = zooms - 1 - z
            zpath = tile_path + '/{}'.format(zlevel)
            print('Generate Zoom: {}'.format(zpath))

            # shrink image
            if zimgs[zlevel] is None:
                zimgs[zlevel] = zimgs[zlevel + 1].resize((sz[0] >> z, sz[1] >> z), Image.LANCZOS)

            if not os.path.isdir(zpath):
                for x in range(0, 2 ** zlevel):
                    dpath = os.path.join(zpath, '{}'.format(x))
                    os.makedirs(dpath, exist_ok=True)
                    for y in range(0, 2 ** zlevel):
                        fpath = os.path.join(dpath, '{}.png'.format(y))
                        zimgs[zlevel].crop((x * tile_size, y * tile_size, (x + 1) * tile_size, (y + 1) * tile_size)).save(
                            fpath)

        for zlevel in range(zooms, max_zoom+1):
            width = tile_size >> (zlevel - (zooms-1))
            zpath = os.path.join(tile_path, '{}'.format(zlevel))
            print('Generate Zoom: {}'.format(zpath))
            if not os.path.isdir(zpath):
                for x in range(0, 2 ** zlevel):
                    dpath = os.path.join(zpath, '{}'.format(x))
                    os.makedirs(dpath, exist_ok=True)
                    for y in range(0, 2 ** zlevel):
                        fpath = os.path.join(dpath, '{}.png'.format(y))
                        zimgs[(zooms-1)].crop((x * width, y * width, (x + 1) * width, (y + 1) * width)).resize((tile_size, tile_size), Image.NEAREST).save(fpath)

    def make_web_map(self, wdir, copy_support_files):
        force_topo_tiles = False

        # BUILD topo map
        topo_dst_path = wdir + 'map/z0/tile_t'
        if not os.path.isdir(topo_dst_path) or force_topo_tiles:  # this is slow so only do it once
            # extract full res image
            ai = []
            for i in range(16):
                ai.append([None] * 16)
            for i in range(256):
                x = i % 16
                y = i // 16
                fn = 'textures/ui/map_reserve_0/zoom3/{}.ddsc'.format(i)
                fn = fn.encode('ascii')
                vnode = self.vfs.map_vpath_to_vfsnodes[fn][0]
                img = Ddsc()
                with self.vfs.file_obj_from(vnode) as f:
                    img.load_ddsc(f)
                ai[y][x] = img.mips[0].data

            for i in range(16):
                ai[i] = np.hstack(ai[i])
            ai = np.vstack(ai)
            img = Image.fromarray(ai)

            self.tileset_make(img, topo_dst_path)

        # BUILD warboard map
        topo_dst_path = wdir + 'map/z0/tile_wb'
        if not os.path.isdir(topo_dst_path) or force_topo_tiles:  # this is slow so only do it once
            # extract full res image
            ai = []
            for i in range(16):
                ai.append([None] * 16)
            for i in range(256):
                x = i % 16
                y = i // 16
                fn = 'textures/ui/warboard_map/zoom3/{}.ddsc'.format(i)
                fn = fn.encode('ascii')
                vnode = self.vfs.map_vpath_to_vfsnodes[fn][0]
                img = Ddsc()
                with self.vfs.file_obj_from(vnode) as f:
                    img.load_ddsc(f)
                ai[y][x] = img.mips[0].data

            for i in range(16):
                ai[i] = np.hstack(ai[i])
            ai = np.vstack(ai)
            img = Image.fromarray(ai)

            self.tileset_make(img, topo_dst_path)

        # BUILD height map
        # extract full res image
        fn = b'terrain/global_heightfield.rawc'
        vnode = self.vfs.map_vpath_to_vfsnodes[fn][0]

        with self.vfs.file_obj_from(vnode) as f:
            buffer = f.read(1024 * 1024)

        aimg = np.frombuffer(buffer, count=512*512, dtype=np.float32)
        aimg = np.reshape(aimg, (512, 512))
        aimg = (aimg - aimg.min()) / (aimg.max() - aimg.min())

        # convert range of values to color map
        cm = plt.get_cmap('jet')
        cimg = cm(aimg)
        img = Image.fromarray((cimg[:, :, :3] * 255).astype(np.uint8))

        self.tileset_make(img, os.path.join(wdir, 'map', 'z0', 'tile_h'))

        # BUILD water nvwaveworks map
        # extract full res image
        fn = b'terrain/water_nvwaveworks_mod.rawc'
        vnode = self.vfs.map_vpath_to_vfsnodes[fn][0]

        with self.vfs.file_obj_from(vnode) as f:
            buffer = f.read(1024 * 1024)

        aimg = np.frombuffer(buffer, count=1024*1024, dtype=np.uint8)
        aimg = np.flipud(np.reshape(aimg, (1024, 1024)).astype(dtype=np.float32))
        aimg = (aimg - aimg.min()) / (aimg.max() - aimg.min())

        # convert range of values to color map
        cm = plt.get_cmap('jet')
        cimg = cm(aimg)
        img = Image.fromarray((cimg[:, :, :3] * 255).astype(np.uint8))

        self.tileset_make(img, os.path.join(wdir, 'map', 'z0', 'tile_wn'))

        # BUILD water gerstner map
        # extract full res image
        fn = b'terrain/water_gerstner_mod.rawc'
        vnode = self.vfs.map_vpath_to_vfsnodes[fn][0]

        with self.vfs.file_obj_from(vnode) as f:
            buffer = f.read(1024 * 1024)

        aimg = np.frombuffer(buffer, count=1024*1024, dtype=np.uint8)
        aimg = np.flipud(np.reshape(aimg, (1024, 1024)).astype(dtype=np.float32))
        aimg = (aimg - aimg.min()) / (aimg.max() - aimg.min())

        # convert range of values to color map
        cm = plt.get_cmap('jet')
        cimg = cm(aimg)
        img = Image.fromarray((cimg[:, :, :3] * 255).astype(np.uint8))

        self.tileset_make(img, os.path.join(wdir, 'map', 'z0', 'tile_wg'))

        # TODO parse terrain/nv_water_cull_mask.rawc ? 1 bit per pixel 512x512 pixels
        fn = b'terrain/nv_water_cull_mask.rawc'
        vnode = self.vfs.map_vpath_to_vfsnodes[fn][0]

        with self.vfs.file_obj_from(vnode) as f:
            buffer = f.read(32 * 1024)

        aimg = np.frombuffer(buffer, count=32*1024, dtype=np.uint8)
        cimg = np.zeros((512, 512, 4), dtype=np.uint8)

        for r in range(512):
            rd = aimg[r*64:(r+1)*64]
            for c in range(64):
                for sc in range(8):
                    if rd[c] & (0x80 >> sc) == 0:
                        cimg[r, c * 8 + sc, :] = [0, 0, 0, 0]
                    else:
                        cimg[r, c*8 + sc, :] = [0xff, 0xff, 0xff, 0xff]
        cimg = np.flip(cimg, 0)
        img = Image.fromarray(cimg)

        self.tileset_make(img, os.path.join(wdir, 'map', 'z0', 'tile_wnm'))

        tile_overlays = []

        for crit in ['dreadnought', 'harvester', 'hunter', 'scout', 'skirmisher']:
            for ctype, color in zip(['a', 'b', 'c', 'd'], [[255, 0, 0, 255], [0, 255, 0, 255], [0, 0, 255, 255], [255, 0, 255, 255]]):
                tile_overlays.append([
                    'settings/hp_settings/hp_ai_textures/spawn_maps/spawn_{}_{}.bmp_datac'.format(crit, ctype).encode('ascii'),
                    'tile_spawn_{}_{}'.format(crit, ctype),
                    color
                ])

        tile_overlays.append([
            'settings/hp_settings/hp_ai_textures/bitmaps/dreadnought_forbidden_map.bmp_datac'.encode('ascii'),
            'tile_bitmap_dreadnought_forbidden_map',
            [255, 0, 0, 255]
        ])

        tile_overlays.append([
            'settings/hp_settings/hp_ai_textures/bitmaps/flee_reserve_0.bmp_datac'.encode('ascii'),
            'tile_bitmap_flee_reserve_0',
            [0, 255, 0, 255]
        ])

        tile_overlays.append([
            'settings/hp_settings/hp_ai_textures/bitmaps/animal_forbidden_map_0.bmp_datac'.encode('ascii'),
            'tile_bitmap_animal_forbidden_map_0',
            [0, 0, 255, 255]
        ])

        for tileo in tile_overlays:
            fn = tileo[0]
            vnode = self.vfs.map_vpath_to_vfsnodes[fn][0]

            with self.vfs.file_obj_from(vnode) as f:
                if vnode.ftype == FTYPE_ADF:
                    buffer = f.read(vnode.size_u)
                    bmp_adf = self.vfs.adf_db.load_adf(buffer)
                else:
                    buffer = f.read(vnode.offset + vnode.size_u)
                    bmp_adf = self.vfs.adf_db.load_adf_bare(buffer, vnode.adf_type, vnode.offset, vnode.size_u)

            bitfield = bmp_adf.table_instance_values[0]['Layers'][0]['Bitfield']
            bitfield = np.asarray(bitfield, dtype=np.uint32).data

            aimg = np.frombuffer(bitfield, count=8 * 1024, dtype=np.uint8)
            cimg = np.zeros((512, 512, 4), dtype=np.uint8)

            for r in range(256):
                rd = aimg[r * 32:(r + 1) * 32]
                # print(*['{:02X}'.format(v) for v in rd])
                for c in range(32):
                    for sc in range(8):
                        if rd[c] & (0x01 << sc) == 0:
                            cimg[128 + r, 128 + c * 8 + sc, :] = [0, 0, 0, 0]
                        else:
                            cimg[128 + r, 128 + c * 8 + sc, :] = tileo[2]
            # cimg = np.flip(cimg, 0)
            img = Image.fromarray(cimg)

            self.tileset_make(img, os.path.join(wdir, 'map', 'z0', '{}'.format(tileo[1])))

        # load translation
        vnode = self.vfs.map_vpath_to_vfsnodes[b'text/master_eng.stringlookup'][0]
        with self.vfs.file_obj_from(vnode, 'rb') as f:
            tr = process_translation_adf(self.vfs, f, vnode.size_u)

        # LOAD from global/collection.collectionc
        # todo dump of different vnodes, one in gdcc is stripped
        vnode = self.vfs.map_vpath_to_vfsnodes[b'global/collection.collectionc'][0]
        adf = adf_node_read(self.vfs, vnode)
        collectables = []
        for v in adf.table_instance_values[0]['Collectibles']:
            obj_id = v['ID']
            cid = v['Name'].decode('utf-8')
            name = cid
            if name in tr:
                name = tr[name]
            else:
                name = name + "_name"
                name = tr.get(name, name)
            desc = cid + '_desc'
            desc = tr.get(desc, desc)
            position = v['Position']
            x = (position[0]) * src_to_dst_x_scale + dst_x0
            y = (position[2]) * src_to_dst_y_scale + dst_y0
            coords = [x, y]

            obj = {
                'type': 'Feature',
                'properties': {
                    'type': 'collection.collectionc',
                    'uid': obj_id,
                    'uid_str': '0x{:012X}'.format(obj_id),
                    'collectable_id': cid,
                    'collectable_name_tr': name,
                    'collectable_desc_tr': desc,
                    'position': position,
                },
                'geometry': {
                    'type': 'Point',
                    'coordinates': coords
                },
            }
            collectables.append(obj)

        # get all mdic AABBs
        print('PROCESSING: mdics')
        mdic_expr = re.compile(rb'^.*mdic$')
        mdics = []
        for fn, vnodes in self.vfs.map_vpath_to_vfsnodes.items():
            if mdic_expr.match(fn) and len(vnodes) > 0:
                print('PROCESSING: {}'.format(fn))
                vnode = vnodes[0]
                with self.vfs.file_obj_from(vnode, 'rb') as f:
                    buffer = f.read(vnode.size_u)
                    adf = self.vfs.adf_db.load_adf(buffer)
                    aabb = AABB(all6=adf.table_instance_values[0]['AABB'])
                    border = [
                        [aabb.min[0], aabb.min[2]],
                        [aabb.max[0], aabb.min[2]],
                        [aabb.max[0], aabb.max[2]],
                        [aabb.min[0], aabb.max[2]],
                    ]

                    coords = []
                    for pt in border:
                        x = pt[0] * src_to_dst_x_scale + dst_x0
                        y = pt[1] * src_to_dst_y_scale + dst_y0
                        coords.append([x, y])

                    obj = {
                        'type': 'Feature',
                        'properties': {
                            'type': 'mdic',
                            'uid': vnode.vhash,
                            'uid_str': vnode.vpath.decode('utf-8'),
                            'comment': '',
                        },
                        'geometry': {
                            'type': 'Polygon',
                            'coordinates': [coords]
                        },
                    }
                    mdics.append(obj)

        print('PROCESSING: blo(s)')
        visitor = RtpcLootVisitor(tr=tr)
        blo_expr = re.compile(rb'^.*blo$')
        for fn, vnodes in self.vfs.map_vpath_to_vfsnodes.items():
            if blo_expr.match(fn) and len(vnodes) > 0:
                print('PROCESSING: {}'.format(fn))
                vnode = vnodes[0]
                with self.vfs.file_obj_from(vnode, 'rb') as f:
                    rtpc = Rtpc()
                    rtpc.deserialize(f)
                rtpc.visit(visitor)

        # results from found rtpc records
        print('Region: count = {}'.format(len(visitor.regions)))
        print('Collectables: count = {}'.format(len(collectables)))
        print('MDICs: count = {}'.format(len(mdics)))
        for k, v in visitor.points.items():
            print('{}: count = {}'.format(k, len(v)))

        # write results
        dpath = os.path.join(wdir, 'map', 'z0')
        os.makedirs(dpath, exist_ok=True)

        fpath = os.path.join(dpath, 'data_full.js')
        with open(fpath, 'w') as f:
            f.write('var region_data = {};\n'.format(json.dumps(visitor.regions, indent=4)))
            f.write('var collectable_data = {};\n'.format(json.dumps(collectables, indent=4)))
            f.write('var mdic_data = {};\n'.format(json.dumps(mdics, indent=4)))
            f.write('var c_collectable_data = {};\n'.format(json.dumps(visitor.points['CCollectable'], indent=4)))
            f.write('var c_book_mark_data = {};\n'.format(json.dumps(visitor.points['CBookMark'], indent=4)))
            f.write('var c_loot_crate_spawn_point_data = {};\n'.format(json.dumps(visitor.points['CLootCrateSpawnPoint'], indent=4)))
            f.write('var c_loot_crate_spawn_point_group_data = {};\n'.format(json.dumps(visitor.points['CLootCrateSpawnPointGroup'], indent=4)))
            f.write('var c_player_spawn_point_data = {};\n'.format(json.dumps(visitor.points['CPlayerSpawnPoint'], indent=4)))
            f.write('var c_poi = {};\n'.format(json.dumps(visitor.points['CPOI'], indent=4)))
            f.write('var c_poi_nest_marker_poi = {};\n'.format(json.dumps(visitor.points['CPOI.nest_marker_poi'], indent=4)))

        fpath = os.path.join(dpath, 'data.js')
        with open(fpath, 'w') as f:
            f.write('var collectable_data = {};\n'.format(json.dumps(collectables, indent=4)))

        if copy_support_files:
            dst = os.path.join(dpath, 'index.html')
            if os.path.exists(dst):
                print('WARNING: {} already exists will not over-write'.format(dst))
            else:
                shutil.copyfile(os.path.join('.', 'tool_resources', 'make_web_map', 'index.html'), dst)

            dst = os.path.join(dpath, 'full.html')
            if os.path.exists(dst):
                print('WARNING: {} already exists will not over-write'.format(dst))
            else:
                shutil.copyfile(os.path.join('.', 'tool_resources', 'make_web_map', 'full.html'), dst)

            dst = os.path.join(dpath, 'lib')
            if os.path.exists(dst):
                print('WARNING: {} already exists will not over-write'.format(dst))
            else:
                shutil.copytree(os.path.join('.', 'tool_resources', 'make_web_map', 'lib'), dst)


def main():
    tool = ToolMakeWebMap('../../../work/gz/project.json')
    # tool = ToolMakeWebMap('../work/gz/project.json')
    tool.make_web_map(tool.vfs.working_dir, False)


if __name__ == "__main__":
    main()


# def export_map():
#     ai = []
#     for i in range(16):
#         ai.append([None] * 16)
#     for i in range(256):
#         x = i % 16
#         y = i // 16
#         fn = 'textures/ui/map_reserve_0/zoom3/{}.ddsc'.format(i)
#         fn = fn.encode('ascii')
#         vnode = vfs_global.map_vpath_to_vfsnodes[fn][0]
#         img = Ddsc()
#         with vfs_global.file_obj_from(vnode) as f:
#             img.load_ddsc(f)
#         ai[y][x] = img.mips[0].data
#
#     import numpy as np
#     from PIL import Image
#     for i in range(16):
#         ai[i] = np.hstack(ai[i])
#     ai = np.vstack(ai)
#     img = Image.fromarray(ai)
#     img.save(working_dir + '/z0.png')
#
#     return img
