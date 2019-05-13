# -*- coding: UTF-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import csv
import glob
import os
import types

import xlsxwriter
from xlrd import *

import file_util
import type_util


def xls_filename_ext():
    """
    获取xls文件扩展名。
    :return:
    """

    return '.xlsx'


def xls_row_pos(row):
    """
    获取xls文件中指定行的位置。
    :param row: 行的index，>=0。
    :return:
    """

    return str(row + 1)


def xls_col_pos(col):
    """
    获取xls文件中指定列的位置。
    :param col: 列的index，>=0。
    :return:
    """

    col += 1

    if col > 26:
        return chr((col - 1) / 26 + 64) + chr((col - 1) % 26 + 65)
    else:
        return chr(col + 64)


def xls_cell_pos(row, col):
    """
    获取xls文件中一个cell的位置字符串。
    :param row: 行的index，>=0。
    :param col: 列的index，>=0。
    :return:
    """

    return '%s,%s' % (xls_row_pos(row), xls_col_pos(col))


def convert_csv_to_xls(csv_file_path, output_dir):
    """
    将csv文件转换成xls文件。
    :param csv_file_path: csv文件路径或者csv文件所在的目录。
    :param output_dir: 输出目录。
    :return: =0表示成功，否则失败。
    """

    if not os.path.exists(csv_file_path):
        print('csv file %s not exist' % csv_file_path)
        return -1

    if os.path.isfile(csv_file_path):
        if file_util.make_dir(output_dir) != 0:
            print('failed to make output dir %s' % output_dir)
            return -1

        base_filename = file_util.base_filename(csv_file_path)
        xls_file_path = '%s%s%s%s' % (output_dir, os.path.sep, base_filename, xls_filename_ext())

        try:
            workbook = xlsxwriter.Workbook(xls_file_path)
            worksheet = workbook.add_worksheet()

            with open(csv_file_path, 'rb') as f:
                csv_content = csv.reader(f)

                for row_idx, row in enumerate(csv_content):
                    for col_idx, cell in enumerate(row):
                        worksheet.write(row_idx, col_idx, cell.strip().decode('utf-8'))

            workbook.close()

            print('=== convert ' + csv_file_path + ' to ' + xls_file_path + ' done ===')
            return 0
        except Exception as e:
            print('exception: %s' % e)
            return -1
    else:
        sub_csv_file_path_list = glob.glob(csv_file_path + os.path.sep + '*.csv')

        if 0 == len(sub_csv_file_path_list):
            return -1

        for i, f in enumerate(sub_csv_file_path_list):
            convert_csv_to_xls(f, output_dir)

    return 0


class XlsCell(object):
    """
    xls单元格    
    """

    def __init__(self, row, col, content):
        self.row = row
        self.col = col
        self.content = content

    def show(self):
        print('%s (%s)' % (str(self.content), xls_cell_pos(self.row, self.col)))


class XlsRow(object):
    """
    xls行，由若干单元格构成
    """

    def __init__(self):
        self.h_cell_list = []

    def __del__(self):
        del self.h_cell_list[:]

    def append(self, xls_cell):
        self.h_cell_list.append(xls_cell)

    def get_cell(self, col):
        if not self.h_cell_list or col < 0 or col >= len(self.h_cell_list):
            return None
        else:
            return self.h_cell_list[col]

    def show(self):
        if 0 == len(self.h_cell_list):
            print('xls row is empty')
        else:
            for xls_cell in self.h_cell_list:
                xls_cell.show()


class XlsCol(object):
    """
    xls列，由若干单元格构成
    """

    def __init__(self):
        self.v_cell_list = []

    def __del__(self):
        del self.v_cell_list[:]

    def append(self, xls_cell):
        self.v_cell_list.append(xls_cell)

    def get_cell(self, row):
        if not self.v_cell_list or row < 0 or row >= len(self.v_cell_list):
            return None
        else:
            return self.v_cell_list[row]

    def show(self):
        if 0 == len(self.v_cell_list):
            print('xls col is empty')
        else:
            for xls_cell in self.v_cell_list:
                xls_cell.show()


class XlsRowGrid(object):
    """
    xls行列表，由若干行构成
    """

    def __init__(self):
        self.row_list = []

    def __del__(self):
        del self.row_list[:]

    def append(self, xls_row):
        self.row_list.append(xls_row)

    def get_row(self, row):
        if not self.row_list or row < 0 or row >= len(self.row_list):
            return None
        else:
            return self.row_list[row]

    def get_cell(self, row, col):
        xls_row = self.get_row(row)

        if not xls_row:
            return None
        else:
            return xls_row.get_cell(col)

    def show(self):
        if 0 == len(self.row_list):
            print('xls row grid is empty')
        else:
            for xls_row in self.row_list:
                xls_row.show()


class XlsColGrid(object):
    """
    xls列列表，由若干列构成
    """

    def __init__(self):
        self.col_list = []

    def __del__(self):
        del self.col_list[:]

    def append(self, xls_col):
        self.col_list.append(xls_col)

    def get_col(self, col):
        if not self.col_list or col < 0 or col >= len(self.col_list):
            return None
        else:
            return self.col_list[col]

    def get_cell(self, row, col):
        xls_col = self.get_col(col)

        if not xls_col:
            return None
        else:
            return xls_col.get_cell(row)

    def show(self):
        if 0 == len(self.col_list):
            print('xls col grid is empty')
        else:
            for xls_col in self.col_list:
                xls_col.show()


class XlsHeadInterface(object):
    """
    xls head interface，用于设置xls文件的行数、列数、各列的类型。
    """

    def init(self, nrows, conf):
        self.nrows = nrows  # head的行数
        self.ncols = len(conf)  # head的列数

        # 下面的代码是必须的，在load xls文件内容的时候会用到col_types
        self.col_types = [1] * self.ncols  # 各列的类型列表，这里先初始化

        for k, v in conf.iteritems():
            self.col_types[v['col']] = v['type']


class XlsLoader(object):
    """
    xls文件内容loader，用于从读取xls文件的内容到内存中。
    """

    def __init__(self, csv_file_path, head_nrows, head_ncols, col_types):
        """

        :param csv_file_path:
        :param head_nrows: head包含的行数
        :param head_ncols: head包含的列数
        :param col_types: 每列的类型，形如[types.StringType, types.StringType, types.StringType, types.BooleanType]，对应各列的类型
        """

        self.csv_file_path = csv_file_path
        self.head_nrows = head_nrows
        self.head_ncols = head_ncols
        self.col_types = col_types
        self.row_grid = XlsRowGrid()  # row grid形式的文件内容
        self.col_grid = XlsColGrid()  # col grid形式的文件内容

    def load(self):
        """
        加载文件内容到内存中，会分别以row grid和col grid的形式保存两份，方便访问。
        :return: 
        """
        try:
            output_dir = file_util.file_dir(self.csv_file_path)
            xls_file_path = '%s%s%s%s' % (output_dir, os.path.sep,
                                          file_util.base_filename(self.csv_file_path), xls_filename_ext())

            if convert_csv_to_xls(self.csv_file_path, output_dir) != 0:
                print('failed to convert %s to %s' % (self.csv_file_path, xls_file_path))
                return -1

            workbook = open_workbook(xls_file_path)
            worksheet = workbook.sheet_by_index(0)

            if worksheet.nrows <= self.head_nrows:
                print("not enough rows")
                return -1

            if worksheet.ncols < self.head_ncols:
                print("not enough cols")
                return -1

            # 按行组织
            for row in range(self.head_nrows, worksheet.nrows):
                xls_row = XlsRow()

                for col in range(0, self.head_ncols):
                    xls_cell = XlsCell(row, col,
                                       type_util.value(self.col_types[col])(worksheet.cell_value(row, col)))
                    xls_row.append(xls_cell)

                self.row_grid.append(xls_row)

            # self.content_row_grid.show()

            # 按列组织
            for col in range(0, self.head_ncols):
                xls_col = XlsCol()

                for row in range(self.head_nrows, worksheet.nrows):
                    xls_cell = XlsCell(row, col,
                                       type_util.value(self.col_types[col])(worksheet.cell_value(row, col)))
                    xls_col.append(xls_cell)

                self.col_grid.append(xls_col)

            # self.content_col_grid.show()

            file_util.del_file(xls_file_path)
            return 0
        except Exception as e:
            print('exception: %s' % e)
            return -1


def demo001():
    for row in range(0, 54):
        assert str(row + 1) == xls_row_pos(row)

    assert 'A' == xls_col_pos(0)
    assert 'Z' == xls_col_pos(25)
    assert 'AA' == xls_col_pos(26)
    assert 'BA' == xls_col_pos(52)


def demo002():
    ret = convert_csv_to_xls(sys.path[0] + '/../data/third_party.csv', sys.path[0] + '/../data')
    assert 0 == ret

    ret = convert_csv_to_xls(sys.path[0] + '/../data', sys.path[0] + '/../data')
    assert 0 == ret


def demo003():
    xls_loader = XlsLoader(sys.path[0] + '/../data/third_party.csv', 1, 4,
                           [types.StringType, types.StringType, types.StringType, types.BooleanType])
    assert 0 == xls_loader.load()


if __name__ == '__main__':
    demo001()
    demo002()
    demo003()
