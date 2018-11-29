# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import os
import sys

sys.path.append('%s/../../py_tools' % os.path.split(os.path.realpath(__file__))[0])  # 导入上级目录中的模块
# print(sys.path)

from base import file_util, xls_util, name_style_util
import xls_head


def output_file_header(fp, xls_head_, xls_row_grid, xls_col_grid, indent):
    content = '''#ifndef XX_CONF_MGR_H_
#define XX_CONF_MGR_H_

#include <string>
#include <vector>
#include "conf_center_interface.h"
#include "conf_mgr_interface.h"
#include "log_util.h"
#include "thread_lock.h"
#include "xx_conf_xpath_define.h"
#include "xx_conf_mgr_interface.h"

namespace xx
{
class ConfMgr : public base::ConfMgrInterface, public ConfMgrInterface
{
public:'''
    fp.write(content.encode('utf-8'))


def output_typedef(fp, xls_head_, xls_row_grid, xls_col_grid, indent):
    table1 = {'int': False, 'int64': False, 'float': False, 'double': False, 'bool': False, 'string': False}
    table2 = {'int': 'typedef std::vector<int> IntGroup;', 'int64': 'typedef std::vector<int64_t> Int64Group;',
              'float': 'typedef std::vector<float> FloatGroup;', 'double': 'typedef std::vector<double> DoubleGroup;',
              'bool': 'typedef std::vector<bool> BoolGroup;', 'string': 'typedef std::vector<std::string> StrGroup;'}

    for xls_row in xls_row_grid.row_list:
        if xls_row.get_cell(xls_head_.conf['group']['col']).content:
            table1[xls_row.get_cell(xls_head_.conf['type']['col']).content] = True

    for k in table1:
        if table1[k]:
            content = [os.linesep,
                       indent, table2[k], os.linesep]
            fp.write(''.join(content).encode('utf-8'))


def output_get_functions(fp, xls_head_, xls_row_grid, xls_col_grid, indent):
    for xls_row in xls_row_grid.row_list:
        name = xls_row.get_cell(xls_head_.conf['name']['col']).content

        if xls_row.get_cell(xls_head_.conf['group']['col']).content:
            return_value = '%s_group_' % name
        else:
            return_value = '%s_' % name

        if xls_row.get_cell(xls_head_.conf['type']['col']).content == 'int':
            if not xls_row.get_cell(xls_head_.conf['group']['col']).content:
                return_type = 'int'
                func_name = 'Get%s' % (name_style_util.underline_to_camel(name))
            else:
                return_type = 'IntGroup'
                func_name = 'Get%sGroup' % (name_style_util.underline_to_camel(name))
        elif xls_row.get_cell(xls_head_.conf['type']['col']).content == 'int64':
            if not xls_row.get_cell(xls_head_.conf['group']['col']).content:
                return_type = 'int64_t'
                func_name = 'Get%s' % (name_style_util.underline_to_camel(name))
            else:
                return_type = 'Int64Group'
                func_name = 'Get%sGroup' % (name_style_util.underline_to_camel(name))
        elif xls_row.get_cell(xls_head_.conf['type']['col']).content == 'float':
            if not xls_row.get_cell(xls_head_.conf['group']['col']).content:
                return_type = 'float'
                func_name = 'Get%s' % (name_style_util.underline_to_camel(name))
            else:
                return_type = 'FloatGroup'
                func_name = 'Get%sGroup' % (name_style_util.underline_to_camel(name))
        elif xls_row.get_cell(xls_head_.conf['type']['col']).content == 'double':
            if not xls_row.get_cell(xls_head_.conf['group']['col']).content:
                return_type = 'double'
                func_name = 'Get%s' % (name_style_util.underline_to_camel(name))
            else:
                return_type = 'DoubleGroup'
                func_name = 'Get%sGroup' % (name_style_util.underline_to_camel(name))
        elif xls_row.get_cell(xls_head_.conf['type']['col']).content == 'bool':
            if not xls_row.get_cell(xls_head_.conf['group']['col']).content:
                return_type = 'bool'
                func_name = '%s' % (name_style_util.underline_to_camel(name))
            else:
                return_type = 'BoolGroup'
                func_name = '%sGroup' % (name_style_util.underline_to_camel(name))
        elif xls_row.get_cell(xls_head_.conf['type']['col']).content == 'string':
            if not xls_row.get_cell(xls_head_.conf['group']['col']).content:
                return_type = 'std::string'
                func_name = 'Get%s' % (name_style_util.underline_to_camel(name))
            else:
                return_type = 'StrGroup'
                func_name = 'Get%sGroup' % (name_style_util.underline_to_camel(name))

        if not xls_row.get_cell(xls_head_.conf['virtual']['col']).content:
            content = [indent, return_type, ' ', func_name, '()', os.linesep,
                       indent, '{', os.linesep,
                       indent * 2, 'AUTO_THREAD_RLOCK(rwlock_);', os.linesep,
                       indent * 2, 'return ', return_value, ';', os.linesep,
                       indent, '}', os.linesep * 2]

        else:
            content = [indent, '', return_type, ' ', func_name, '() override', os.linesep,
                       indent, '{', os.linesep,
                       indent * 2, 'AUTO_THREAD_RLOCK(rwlock_);', os.linesep,
                       indent * 2, 'return ', return_value, ';', os.linesep,
                       indent, '}', os.linesep * 2]

        fp.write(''.join(content).encode('utf-8'))


def output_load_function(fp, xls_head_, xls_row, indent):
    table1 = {'int': 'int', 'int64': 'int64_t', 'float': 'float', 'double': 'double', 'bool': 'int', 'string': 'char*'}
    name = xls_row.get_cell(xls_head_.conf['name']['col']).content
    table2 = {'int': '%sif (conf_center_->GetConf(%s_, ' % (indent * 2, name),
              'int64': '%sif (conf_center_->GetConf(%s_, ' % (indent * 2, name),
              'float': '%sif (conf_center_->GetConf(%s_, ' % (indent * 2, name),
              'double': '%sif (conf_center_->GetConf(%s_, ' % (indent * 2, name),
              'bool': '%sif (conf_center_->GetConf(%s, ' % (indent * 2, name),
              'string': '%sif (conf_center_->GetConf(&%s, ' % (indent * 2, name)}
    # bool
    table_bool_1 = {'int': '', 'int64': '', 'float': '', 'double': '',
                    'bool': '%sint %s = 0;%s' % (indent * 2, name, os.linesep),
                    'string': ''}
    table_bool_2 = {'int': '', 'int64': '', 'float': '', 'double': '',
                    'bool': '%s%s_ = (%s != 0);%s' % (indent * 2, name, name, os.linesep),
                    'string': ''}

    table3 = {'int': '%sconf_center_->ReleaseConf(&%s);%s' % (indent * 3, name, os.linesep),
              'int64': '%sconf_center_->ReleaseConf(&%s);%s' % (indent * 3, name, os.linesep),
              'float': '%sconf_center_->ReleaseConf(&%s);%s' % (indent * 3, name, os.linesep),
              'double': '%sconf_center_->ReleaseConf(&%s);%s' % (indent * 3, name, os.linesep),
              'bool': '%sconf_center_->ReleaseConf(&%s);%s' % (indent * 3, name, os.linesep),
              'string': '%sconf_center_->ReleaseConf(&%s, n);%s' % (indent * 3, name, os.linesep)}
    table4 = {'int': '%s%s_group_.push_back(%s[i]);%s' % (indent * 3, name, name, os.linesep),
              'int64': '%s%s_group_.push_back(%s[i]);%s' % (indent * 3, name, name, os.linesep),
              'float': '%s%s_group_.push_back(%s[i]);%s' % (indent * 3, name, name, os.linesep),
              'double': '%s%s_group_.push_back(%s[i]);%s' % (indent * 3, name, name, os.linesep),
              'bool': '%s%s_group_.push_back(%s[i] != 0);%s' % (indent * 3, name, name, os.linesep),
              'string': '%s%s_group_.push_back(%s[i]);%s' % (indent * 4, name, name, os.linesep)}
    table5 = {'int': '%s}%s' % (indent * 2, os.linesep),
              'int64': '%s}%s' % (indent * 2, os.linesep),
              'float': '%s}%s' % (indent * 2, os.linesep),
              'double': '%s}%s' % (indent * 2, os.linesep),
              'bool': '%s}%s' % (indent * 2, os.linesep),
              'string': '%s}%s%s}%s' % (indent * 3, os.linesep, indent * 2, os.linesep)}
    table6 = {'int': '%sconf_center_->ReleaseConf(&%s);%s' % (indent * 2, name, os.linesep),
              'int64': '%sconf_center_->ReleaseConf(&%s);%s' % (indent * 2, name, os.linesep),
              'float': '%sconf_center_->ReleaseConf(&%s);%s' % (indent * 2, name, os.linesep),
              'double': '%sconf_center_->ReleaseConf(&%s);%s' % (indent * 2, name, os.linesep),
              'bool': '%sconf_center_->ReleaseConf(&%s);%s' % (indent * 2, name, os.linesep),
              'string': '%sconf_center_->ReleaseConf(&%s, n);%s' % (indent * 2, name, os.linesep)}

    # string
    table_string_1 = {'int': '', 'int64': '', 'float': '', 'double': '', 'bool': '',
                      'string': '%schar* %s = NULL;%s' % (indent * 2, name, os.linesep)}
    table_string_2 = {'int': '', 'int64': '', 'float': '', 'double': '', 'bool': '',
                      'string': '%sconf_center_->ReleaseConf(&%s);%s' % (indent * 3, name, os.linesep)}
    table_string_3 = {'int': '', 'int64': '', 'float': '', 'double': '', 'bool': '',
                      'string': '%s%s_ = %s;%s%sconf_center_->ReleaseConf(&%s);%s' % (
                      indent * 2, name, name, os.linesep, indent * 2, name, os.linesep)}
    table_string_4 = {'int': '', 'int64': '', 'float': '', 'double': '', 'bool': '',
                      'string': '%sif (strlen(%s[i]) > 0)%s%s{%s' % (
                      indent * 3, name, os.linesep, indent * 3, os.linesep)}

    if not xls_row.get_cell(xls_head_.conf['with_default']['col']).content:
        with_default_str = 'false'
    else:
        with_default_str = 'true, %s' % xls_row.get_cell(xls_head_.conf['default']['col']).content

    type_ = xls_row.get_cell(xls_head_.conf['type']['col']).content
    if not xls_row.get_cell(xls_head_.conf['group']['col']).content:
        content = [table_bool_1[type_],
                   table_string_1[type_],
                   table2[type_], name.upper(), '_XPATH, ',
                   with_default_str, ') != 0)', os.linesep,
                   indent * 2, '{', os.linesep,
                   indent * 3, 'LOG_ERROR("failed to get " << ', name.upper(),
                   '_XPATH << ": " << conf_center_->GetLastErrMsg());', os.linesep,
                   table_string_2[type_],
                   indent * 3, 'return -1;', os.linesep,
                   indent * 2, '}', os.linesep,
                   table_bool_2[type_],
                   table_string_3[type_],
                   indent * 2, 'return 0;', os.linesep]
    else:
        content = [indent * 2, table1[type_], '* ', name,
                   ' = NULL;', os.linesep,
                   indent * 2, 'int n = 0;', os.linesep,
                   indent * 2, 'if (conf_center_->GetConf(&', name, ', n, ',
                   name.upper(), '_XPATH, ', with_default_str, ') != 0)', os.linesep,
                   indent * 2, '{', os.linesep,
                   indent * 3, 'LOG_ERROR("failed to get " << ', name.upper(),
                   '_XPATH << ": " << conf_center_->GetLastErrMsg());', os.linesep,
                   table3[type_],
                   indent * 3, 'return -1;', os.linesep, indent * 2, '}', os.linesep,
                   indent * 2, 'for (int i = 0; i < n; ++i)', os.linesep,
                   indent * 2, '{', os.linesep,
                   table_string_4[type_],
                   table4[type_],
                   table5[type_],
                   table6[type_],
                   indent * 2, 'return 0;', os.linesep]
    fp.write(''.join([i for i in content if len(i) > 0]).encode('utf-8'))


def output_load_functions(fp, xls_head_, xls_row_grid, xls_col_grid, indent):
    content = '''private:
'''
    fp.write(content.encode('utf-8'))

    for xls_row in xls_row_grid.row_list:
        name = xls_row.get_cell(xls_head_.conf['name']['col']).content

        if xls_row.get_cell(xls_head_.conf['group']['col']).content:
            content = '%sint Load%sGroup()%s%s{%s' % (
            indent, name_style_util.underline_to_camel(name), os.linesep, indent, os.linesep)
        else:
            content = '%sint Load%s()%s%s{%s' % (
            indent, name_style_util.underline_to_camel(name), os.linesep, indent, os.linesep)

        fp.write(content.encode('utf-8'))

        output_load_function(fp, xls_head_, xls_row, indent)

        content = [indent, '}', os.linesep * 2]
        fp.write(''.join(content).encode('utf-8'))


def output_variable_declare(fp, xls_head_, xls_row_grid, xls_col_grid, indent):
    content = '''private:
    ThreadRWLock rwlock_;
'''
    fp.write(content.encode('utf-8'))

    for xls_row in xls_row_grid.row_list:
        type_ = xls_row.get_cell(xls_head_.conf['type']['col']).content
        name = xls_row.get_cell(xls_head_.conf['name']['col']).content
        group = xls_row.get_cell(xls_head_.conf['group']['col']).content

        if type_ == 'int':
            if not group:
                variable_type = 'int'
            else:
                variable_type = 'IntGroup'
        elif type_ == 'int64':
            if not group:
                variable_type = 'int64_t'
            else:
                variable_type = 'Int64Group'
        elif type_ == 'float':
            if not group:
                variable_type = 'float'
            else:
                variable_type = 'FloatGroup'
        elif type_ == 'double':
            if not group:
                variable_type = 'double'
            else:
                variable_type = 'DoubleGroup'
        elif type_ == 'bool':
            if not group:
                variable_type = 'bool'
            else:
                variable_type = 'BoolGroup'
        elif type_ == 'string':
            if not group:
                variable_type = 'std::string'
            else:
                variable_type = 'StrGroup'

        if group:
            content = '%s%s %s_group_;%s' % (indent, variable_type, name, os.linesep)
        else:
            content = '%s%s %s_;%s' % (indent, variable_type, name, os.linesep)
        fp.write(content.encode('utf-8'))


def output_content(fp, xls_head_, xls_row_grid, xls_col_grid, indent):
    content = '''#include "xx_conf_mgr.h"

namespace xx
{
ConfMgr::ConfMgr() : rwlock_()
{
}

ConfMgr::~ConfMgr()
{
}

int ConfMgr::Load()
{
    AUTO_THREAD_WLOCK(rwlock_);

'''
    fp.write(content.encode('utf-8'))

    table = {'int': '0', 'int64': '0L', 'float': '0.0F', 'double': 0.0, 'bool': 'false', 'string': '""'}

    for xls_row in xls_row_grid.row_list:
        type_ = xls_row.get_cell(xls_head_.conf['type']['col']).content
        name = xls_row.get_cell(xls_head_.conf['name']['col']).content

        if xls_row.get_cell(xls_head_.conf['group']['col']).content:
            content = '%s%s_group_.clear();%s' % (indent, name, os.linesep)
        else:
            content = '%s%s_ = %s;%s' % (indent, name, table[type_], os.linesep)
        fp.write(content.encode('utf-8'))

    fp.write(os.linesep)

    for xls_row in xls_row_grid.row_list:
        name = xls_row.get_cell(xls_head_.conf['name']['col']).content

        if xls_row.get_cell(xls_head_.conf['group']['col']).content:
            func_name = 'Load%sGroup' % name_style_util.name_style_util.underline_to_camel(name)
        else:
            func_name = 'Load%s' % name_style_util.name_style_util.underline_to_camel(name)

        content = [indent, 'if (', func_name, '() != 0)', os.linesep,
                   indent, '{', os.linesep,
                   indent * 2, 'return -1;', os.linesep,
                   indent, '}', os.linesep * 2]
        fp.write(''.join(content).encode('utf-8'))

    content = '''    return 0;
}
}
'''
    fp.write(content.encode('utf-8'))


def generate_conf_mgr_h_file(xls_head_, xls_row_grid, xls_col_grid, output_dir):
    file_path = os.path.join(output_dir, 'xx_conf_mgr.h')
    file_util.del_file(file_path)
    file_util.make_dir(output_dir)

    try:
        fp = open(file_path, "wb")

        output_file_header(fp, xls_head_, xls_row_grid, xls_col_grid, '')

        indent = ' ' * 4
        # output_typedef(fp, xls_head_, xls_row_grid, xls_col_grid, indent)

        content = '''
    ConfMgr();
    virtual ~ConfMgr();

private:
    ///////////////////////// base::ConfMgrInterface /////////////////////////
    virtual int Load();

public:
    ///////////////////////// ConfMgrInterface /////////////////////////
'''
        fp.write(content.encode('utf-8'))

        output_get_functions(fp, xls_head_, xls_row_grid, xls_col_grid, indent)
        output_load_functions(fp, xls_head_, xls_row_grid, xls_col_grid, indent)
        output_variable_declare(fp, xls_head_, xls_row_grid, xls_col_grid, indent)

        content = '''};
}

#endif // XX_CONF_MGR_H_
'''
        fp.write(content.encode('utf-8'))

        fp.close()

        # file_util.replace_content(file_path, ["Tcp TCP", "Io IO", "Cpu CPU", "Udp UDP"])
        print('=== generate %s done ===' % file_path)

        return 0
    except Exception as e:
        print('exception: %s' % e)
        return -1


def test_001():
    xls_head_ = xls_head.XlsHead()
    xls_loader = xls_util.XlsLoader('./app_frame_conf.csv', xls_head_.nrows, xls_head_.ncols, xls_head_.col_types)
    assert 0 == xls_loader.load()
    assert 0 == generate_conf_mgr_h_file(xls_head_, xls_loader.row_grid, xls_loader.col_grid, './output/app_frame')


if __name__ == "__main__":
    test_001()
