# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from .dataviewwidget import DataViewWidget


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(960, 603)
        self.action_project_new = QAction(MainWindow)
        self.action_project_new.setObjectName(u"action_project_new")
        self.action_project_open = QAction(MainWindow)
        self.action_project_open.setObjectName(u"action_project_open")
        self.action_external_add = QAction(MainWindow)
        self.action_external_add.setObjectName(u"action_external_add")
        self.action_exit = QAction(MainWindow)
        self.action_exit.setObjectName(u"action_exit")
        self.action_make_web_map = QAction(MainWindow)
        self.action_make_web_map.setObjectName(u"action_make_web_map")
        self.action_file_gz_open = QAction(MainWindow)
        self.action_file_gz_open.setObjectName(u"action_file_gz_open")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(7)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 11, 11, 0)
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(7)
        self.splitter.setChildrenCollapsible(False)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabs_nodes = QTabWidget(self.layoutWidget)
        self.tabs_nodes.setObjectName(u"tabs_nodes")
        self.tabs_nodes.setTabsClosable(True)

        self.verticalLayout.addWidget(self.tabs_nodes)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.filter_label = QLabel(self.layoutWidget)
        self.filter_label.setObjectName(u"filter_label")

        self.horizontalLayout.addWidget(self.filter_label)

        self.filter_edit = QLineEdit(self.layoutWidget)
        self.filter_edit.setObjectName(u"filter_edit")

        self.horizontalLayout.addWidget(self.filter_edit)

        self.filter_set_bt = QPushButton(self.layoutWidget)
        self.filter_set_bt.setObjectName(u"filter_set_bt")

        self.horizontalLayout.addWidget(self.filter_set_bt)

        self.filter_clear_bt = QPushButton(self.layoutWidget)
        self.filter_clear_bt.setObjectName(u"filter_clear_bt")

        self.horizontalLayout.addWidget(self.filter_clear_bt)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tabs_control = QTabWidget(self.layoutWidget)
        self.tabs_control.setObjectName(u"tabs_control")
        self.tab_extract = QWidget()
        self.tab_extract.setObjectName(u"tab_extract")
        self.gridLayout = QGridLayout(self.tab_extract)
        self.gridLayout.setObjectName(u"gridLayout")
        self.cmbbx_map_format = QComboBox(self.tab_extract)
        self.cmbbx_map_format.addItem("")
        self.cmbbx_map_format.addItem("")
        self.cmbbx_map_format.addItem("")
        self.cmbbx_map_format.setObjectName(u"cmbbx_map_format")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbbx_map_format.sizePolicy().hasHeightForWidth())
        self.cmbbx_map_format.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.cmbbx_map_format, 4, 1, 1, 2)

        self.chkbx_export_contents_extract = QCheckBox(self.tab_extract)
        self.chkbx_export_contents_extract.setObjectName(u"chkbx_export_contents_extract")

        self.gridLayout.addWidget(self.chkbx_export_contents_extract, 2, 0, 1, 1)

        self.chkbx_export_text_extract = QCheckBox(self.tab_extract)
        self.chkbx_export_text_extract.setObjectName(u"chkbx_export_text_extract")

        self.gridLayout.addWidget(self.chkbx_export_text_extract, 3, 0, 1, 1)

        self.chkbx_export_map = QCheckBox(self.tab_extract)
        self.chkbx_export_map.setObjectName(u"chkbx_export_map")

        self.gridLayout.addWidget(self.chkbx_export_map, 4, 0, 1, 1)

        self.chkbx_export_raw_extract = QCheckBox(self.tab_extract)
        self.chkbx_export_raw_extract.setObjectName(u"chkbx_export_raw_extract")

        self.gridLayout.addWidget(self.chkbx_export_raw_extract, 0, 0, 1, 1)

        self.chkbx_export_processed_extract = QCheckBox(self.tab_extract)
        self.chkbx_export_processed_extract.setObjectName(u"chkbx_export_processed_extract")

        self.gridLayout.addWidget(self.chkbx_export_processed_extract, 1, 0, 1, 1)

        self.bt_extract = QPushButton(self.tab_extract)
        self.bt_extract.setObjectName(u"bt_extract")
        self.bt_extract.setIconSize(QSize(18, 18))

        self.gridLayout.addWidget(self.bt_extract, 0, 2, 1, 2)

        self.bt_extract_folder_show = QPushButton(self.tab_extract)
        self.bt_extract_folder_show.setObjectName(u"bt_extract_folder_show")
        sizePolicy.setHeightForWidth(self.bt_extract_folder_show.sizePolicy().hasHeightForWidth())
        self.bt_extract_folder_show.setSizePolicy(sizePolicy)
        self.bt_extract_folder_show.setIconSize(QSize(18, 18))

        self.gridLayout.addWidget(self.bt_extract_folder_show, 0, 1, 1, 1)

        self.tab_extract_hspacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.tab_extract_hspacer, 0, 4, 1, 1)

        self.gridLayout.setRowMinimumHeight(0, 28)
        self.gridLayout.setRowMinimumHeight(1, 28)
        self.gridLayout.setRowMinimumHeight(2, 28)
        self.gridLayout.setRowMinimumHeight(3, 28)
        self.gridLayout.setRowMinimumHeight(4, 28)
        self.tabs_control.addTab(self.tab_extract, "")
        self.tab_modding = QWidget()
        self.tab_modding.setObjectName(u"tab_modding")
        self.gridLayout_3 = QGridLayout(self.tab_modding)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.chkbx_export_processed_mods = QCheckBox(self.tab_modding)
        self.chkbx_export_processed_mods.setObjectName(u"chkbx_export_processed_mods")

        self.gridLayout_3.addWidget(self.chkbx_export_processed_mods, 1, 0, 1, 1)

        self.chkbx_mod_build_subset = QCheckBox(self.tab_modding)
        self.chkbx_mod_build_subset.setObjectName(u"chkbx_mod_build_subset")

        self.gridLayout_3.addWidget(self.chkbx_mod_build_subset, 3, 0, 1, 1)

        self.bt_mod_folder_show = QPushButton(self.tab_modding)
        self.bt_mod_folder_show.setObjectName(u"bt_mod_folder_show")
        sizePolicy.setHeightForWidth(self.bt_mod_folder_show.sizePolicy().hasHeightForWidth())
        self.bt_mod_folder_show.setSizePolicy(sizePolicy)
        self.bt_mod_folder_show.setIconSize(QSize(18, 18))

        self.gridLayout_3.addWidget(self.bt_mod_folder_show, 0, 1, 1, 1)

        self.chkbx_export_raw_mods = QCheckBox(self.tab_modding)
        self.chkbx_export_raw_mods.setObjectName(u"chkbx_export_raw_mods")

        self.gridLayout_3.addWidget(self.chkbx_export_raw_mods, 0, 0, 1, 1)

        self.bt_mod_prep = QPushButton(self.tab_modding)
        self.bt_mod_prep.setObjectName(u"bt_mod_prep")
        self.bt_mod_prep.setIconSize(QSize(18, 18))

        self.gridLayout_3.addWidget(self.bt_mod_prep, 0, 2, 1, 1)

        self.bt_mod_build = QPushButton(self.tab_modding)
        self.bt_mod_build.setObjectName(u"bt_mod_build")
        self.bt_mod_build.setIconSize(QSize(18, 18))

        self.gridLayout_3.addWidget(self.bt_mod_build, 1, 2, 1, 1)

        self.chkbx_export_contents_mods = QCheckBox(self.tab_modding)
        self.chkbx_export_contents_mods.setObjectName(u"chkbx_export_contents_mods")

        self.gridLayout_3.addWidget(self.chkbx_export_contents_mods, 2, 0, 1, 1)

        self.bt_mod_build_folder_show = QPushButton(self.tab_modding)
        self.bt_mod_build_folder_show.setObjectName(u"bt_mod_build_folder_show")
        sizePolicy.setHeightForWidth(self.bt_mod_build_folder_show.sizePolicy().hasHeightForWidth())
        self.bt_mod_build_folder_show.setSizePolicy(sizePolicy)
        self.bt_mod_build_folder_show.setIconSize(QSize(18, 18))

        self.gridLayout_3.addWidget(self.bt_mod_build_folder_show, 1, 1, 1, 1)

        self.chkbx_mod_do_not_build_archives = QCheckBox(self.tab_modding)
        self.chkbx_mod_do_not_build_archives.setObjectName(u"chkbx_mod_do_not_build_archives")

        self.gridLayout_3.addWidget(self.chkbx_mod_do_not_build_archives, 4, 0, 1, 3)

        self.tab_modding_hspacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.tab_modding_hspacer, 0, 3, 1, 1)

        self.gridLayout_3.setRowMinimumHeight(0, 28)
        self.gridLayout_3.setRowMinimumHeight(1, 28)
        self.gridLayout_3.setRowMinimumHeight(2, 28)
        self.gridLayout_3.setRowMinimumHeight(3, 28)
        self.gridLayout_3.setRowMinimumHeight(4, 28)
        self.tabs_control.addTab(self.tab_modding, "")
        self.tab_3d_gltf2 = QWidget()
        self.tab_3d_gltf2.setObjectName(u"tab_3d_gltf2")
        self.gridLayout_2 = QGridLayout(self.tab_3d_gltf2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.bt_extract_gltf_3d_folder_show = QPushButton(self.tab_3d_gltf2)
        self.bt_extract_gltf_3d_folder_show.setObjectName(u"bt_extract_gltf_3d_folder_show")
        sizePolicy.setHeightForWidth(self.bt_extract_gltf_3d_folder_show.sizePolicy().hasHeightForWidth())
        self.bt_extract_gltf_3d_folder_show.setSizePolicy(sizePolicy)
        self.bt_extract_gltf_3d_folder_show.setIconSize(QSize(18, 18))

        self.gridLayout_2.addWidget(self.bt_extract_gltf_3d_folder_show, 0, 1, 1, 1)

        self.chkbx_export_save_to_one_dir = QCheckBox(self.tab_3d_gltf2)
        self.chkbx_export_save_to_one_dir.setObjectName(u"chkbx_export_save_to_one_dir")

        self.gridLayout_2.addWidget(self.chkbx_export_save_to_one_dir, 0, 0, 1, 1)

        self.chkbx_export_3d_include_skeleton = QCheckBox(self.tab_3d_gltf2)
        self.chkbx_export_3d_include_skeleton.setObjectName(u"chkbx_export_3d_include_skeleton")

        self.gridLayout_2.addWidget(self.chkbx_export_3d_include_skeleton, 1, 0, 1, 1)

        self.lbl_texture_format = QLabel(self.tab_3d_gltf2)
        self.lbl_texture_format.setObjectName(u"lbl_texture_format")

        self.gridLayout_2.addWidget(self.lbl_texture_format, 3, 0, 1, 1)

        self.bt_extract_gltf_3d = QPushButton(self.tab_3d_gltf2)
        self.bt_extract_gltf_3d.setObjectName(u"bt_extract_gltf_3d")
        self.bt_extract_gltf_3d.setIconSize(QSize(18, 18))

        self.gridLayout_2.addWidget(self.bt_extract_gltf_3d, 0, 2, 1, 2)

        self.cmbbx_texture_format = QComboBox(self.tab_3d_gltf2)
        self.cmbbx_texture_format.addItem("")
        self.cmbbx_texture_format.addItem("")
        self.cmbbx_texture_format.addItem("")
        self.cmbbx_texture_format.setObjectName(u"cmbbx_texture_format")
        sizePolicy.setHeightForWidth(self.cmbbx_texture_format.sizePolicy().hasHeightForWidth())
        self.cmbbx_texture_format.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.cmbbx_texture_format, 3, 1, 1, 2)

        self.tab_3d_hspacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.tab_3d_hspacer, 0, 4, 1, 1)

        self.tab_3d_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.tab_3d_vspacer, 2, 4, 1, 1)

        self.gridLayout_2.setRowMinimumHeight(0, 28)
        self.gridLayout_2.setRowMinimumHeight(1, 28)
        self.gridLayout_2.setRowMinimumHeight(2, 28)
        self.gridLayout_2.setRowMinimumHeight(3, 28)
        self.tabs_control.addTab(self.tab_3d_gltf2, "")
        self.tab_utils = QWidget()
        self.tab_utils.setObjectName(u"tab_utils")
        self.gridLayout_4 = QGridLayout(self.tab_utils)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.vhash_to_vpath_label = QLabel(self.tab_utils)
        self.vhash_to_vpath_label.setObjectName(u"vhash_to_vpath_label")

        self.gridLayout_4.addWidget(self.vhash_to_vpath_label, 0, 0, 1, 1)

        self.vhash_to_vpath_in_edit = QLineEdit(self.tab_utils)
        self.vhash_to_vpath_in_edit.setObjectName(u"vhash_to_vpath_in_edit")

        self.gridLayout_4.addWidget(self.vhash_to_vpath_in_edit, 0, 1, 1, 1)

        self.vhash_to_vpath_out_edit = QLineEdit(self.tab_utils)
        self.vhash_to_vpath_out_edit.setObjectName(u"vhash_to_vpath_out_edit")
        self.vhash_to_vpath_out_edit.setReadOnly(True)

        self.gridLayout_4.addWidget(self.vhash_to_vpath_out_edit, 0, 2, 1, 1)

        self.tab_utils_vspacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_4.addItem(self.tab_utils_vspacer, 1, 2, 1, 1)

        self.gridLayout_4.setColumnStretch(2, 1)
        self.gridLayout_4.setRowMinimumHeight(0, 28)
        self.gridLayout_4.setRowMinimumHeight(1, 28)
        self.tabs_control.addTab(self.tab_utils, "")

        self.verticalLayout.addWidget(self.tabs_control)

        self.verticalLayout.setStretch(0, 1)
        self.splitter.addWidget(self.layoutWidget)
        self.data_view = DataViewWidget(self.splitter)
        self.data_view.setObjectName(u"data_view")
        self.splitter.addWidget(self.data_view)

        self.verticalLayout_2.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 960, 26))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName(u"menu_File")
        self.menu_Tools = QMenu(self.menubar)
        self.menu_Tools.setObjectName(u"menu_Tools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Tools.menuAction())
        self.menu_File.addAction(self.action_project_new)
        self.menu_File.addAction(self.action_project_open)
        self.menu_File.addAction(self.action_file_gz_open)
        self.menu_File.addAction(self.action_external_add)
        self.menu_File.addAction(self.action_exit)
        self.menu_Tools.addAction(self.action_make_web_map)

        self.retranslateUi(MainWindow)

        self.tabs_nodes.setCurrentIndex(-1)
        self.tabs_control.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_project_new.setText(QCoreApplication.translate("MainWindow", u"&New Project...", None))
        self.action_project_open.setText(QCoreApplication.translate("MainWindow", u"&Open Project...", None))
        self.action_external_add.setText(QCoreApplication.translate("MainWindow", u"&Add External...", None))
        self.action_exit.setText(QCoreApplication.translate("MainWindow", u"E&xit", None))
#if QT_CONFIG(shortcut)
        self.action_exit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.action_make_web_map.setText(QCoreApplication.translate("MainWindow", u"Make &Web Map...", None))
        self.action_file_gz_open.setText(QCoreApplication.translate("MainWindow", u"Open GenZero File...", None))
        self.filter_label.setText(QCoreApplication.translate("MainWindow", u"Filter (Python Expression Syntax)", None))
        self.filter_edit.setText("")
        self.filter_set_bt.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.filter_clear_bt.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.cmbbx_map_format.setItemText(0, QCoreApplication.translate("MainWindow", u"Full", None))
        self.cmbbx_map_format.setItemText(1, QCoreApplication.translate("MainWindow", u"Tiles", None))
        self.cmbbx_map_format.setItemText(2, QCoreApplication.translate("MainWindow", u"Full + Tiles", None))

        self.chkbx_export_contents_extract.setText(QCoreApplication.translate("MainWindow", u"Export Contents", None))
        self.chkbx_export_text_extract.setText(QCoreApplication.translate("MainWindow", u"Export As Text", None))
        self.chkbx_export_map.setText(QCoreApplication.translate("MainWindow", u"Export Map", None))
        self.chkbx_export_raw_extract.setText(QCoreApplication.translate("MainWindow", u"Export Raw Files", None))
        self.chkbx_export_processed_extract.setText(QCoreApplication.translate("MainWindow", u"Export As Processed", None))
        self.bt_extract.setText(QCoreApplication.translate("MainWindow", u"EXTRACT", None))
        self.tabs_control.setTabText(self.tabs_control.indexOf(self.tab_extract), QCoreApplication.translate("MainWindow", u"Extract", None))
        self.chkbx_export_processed_mods.setText(QCoreApplication.translate("MainWindow", u"Export As Processed", None))
        self.chkbx_mod_build_subset.setText(QCoreApplication.translate("MainWindow", u"Build Subset", None))
        self.chkbx_export_raw_mods.setText(QCoreApplication.translate("MainWindow", u"Export Raw Files", None))
        self.bt_mod_prep.setText(QCoreApplication.translate("MainWindow", u"Extract For Modding", None))
        self.bt_mod_build.setText(QCoreApplication.translate("MainWindow", u"Build Modded Files", None))
        self.chkbx_export_contents_mods.setText(QCoreApplication.translate("MainWindow", u"Export Contents", None))
        self.chkbx_mod_do_not_build_archives.setText(QCoreApplication.translate("MainWindow", u"Do Not Build Archives", None))
        self.tabs_control.setTabText(self.tabs_control.indexOf(self.tab_modding), QCoreApplication.translate("MainWindow", u"Modding", None))
        self.chkbx_export_save_to_one_dir.setText(QCoreApplication.translate("MainWindow", u"Save To One Directory", None))
        self.chkbx_export_3d_include_skeleton.setText(QCoreApplication.translate("MainWindow", u"Include Skeleton", None))
        self.lbl_texture_format.setText(QCoreApplication.translate("MainWindow", u"Texture Format", None))
        self.bt_extract_gltf_3d.setText(QCoreApplication.translate("MainWindow", u"EXPORT 3D/GLTF2", None))
        self.cmbbx_texture_format.setItemText(0, QCoreApplication.translate("MainWindow", u"dds", None))
        self.cmbbx_texture_format.setItemText(1, QCoreApplication.translate("MainWindow", u"ddsc", None))
        self.cmbbx_texture_format.setItemText(2, QCoreApplication.translate("MainWindow", u"png", None))

        self.tabs_control.setTabText(self.tabs_control.indexOf(self.tab_3d_gltf2), QCoreApplication.translate("MainWindow", u"3d/GLTF2", None))
        self.vhash_to_vpath_label.setText(QCoreApplication.translate("MainWindow", u"VHash -> VPath", None))
        self.vhash_to_vpath_in_edit.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.tabs_control.setTabText(self.tabs_control.indexOf(self.tab_utils), QCoreApplication.translate("MainWindow", u"Utils", None))
        self.menu_File.setTitle(QCoreApplication.translate("MainWindow", u"&File", None))
        self.menu_Tools.setTitle(QCoreApplication.translate("MainWindow", u"&Tools", None))
    # retranslateUi

