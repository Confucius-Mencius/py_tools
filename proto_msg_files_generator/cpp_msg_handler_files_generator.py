# -*- coding: utf-8 -*-

###############################################################################
# author: BrentHuang (guang11cheng@qq.com)
###############################################################################

import os
import sys

sys.path.append('%s/..' % os.path.split(os.path.realpath(__file__))[0])  # 导入上级目录中的模块
# print(sys.path)

from base import file_util, name_style_util
import one_file_msg_mgr


def output_header_file_content(fp, msg, namespace):
    try:
        if 'proto_tcp' == namespace:
            namespace_begin = 'namespace tcp%s{%snamespace proto%s{' % (os.linesep, os.linesep, os.linesep)
            namespace_end = '}%s}' % os.linesep

        guard = 'DEMO_SERVER_%s_LOGICS_%s_HANDLER_H_' % (namespace.upper(),
                                                         name_style_util.camel_to_underline(msg).upper())
        class_name = '%sHandler' % msg

        content = ['#ifndef %s' % guard, os.linesep,
                   '#define %s' % guard, os.linesep * 2,
                   '#include "msg_handler.h"', os.linesep * 2,
                   '%s' % namespace_begin, os.linesep,
                   'class %s : public MsgHandler' % class_name, os.linesep,
                   '{', os.linesep, 'public:', os.linesep,
                   '    %sHandler();' % msg, os.linesep,
                   '    virtual ~%sHandler();' % msg, os.linesep * 2]
        fp.write(''.join(content).encode('utf-8'))

        if namespace == 'proto_tcp':
            content = '''    ///////////////////////// MsgHandlerInterface /////////////////////////
    ::proto::MsgID GetMsgID() override;
    void OnMsg(const ConnGUID* conn_guid, const ::proto::MsgHead& msg_head,
               const void* msg_body, size_t msg_body_len) override;

private:
    void SendErrRsp(const ConnGUID* conn_guid, const ::proto::MsgHead& req_msg_head, int err_code) const;'''
            fp.write(content.encode('utf-8'))
        elif namespace == 'http':
            content = '''    ///////////////////////// http::MsgHandlerInterface /////////////////////////
    const char* GetHttpReqPath() override;
    void OnHttpHeadReq(const ConnGuid* conn_guid, struct evhttp_request* evhttp_req, bool https,
                       const KeyValMap* http_header_map, const KeyValMap* http_query_map) override;
    void OnHttpGetReq(const ConnGuid* conn_guid, struct evhttp_request* evhttp_req, bool https,
                      const KeyValMap* http_header_map, const KeyValMap* http_query_map) override;
    void OnHttpPostReq(const ConnGuid* conn_guid, struct evhttp_request* evhttp_req, bool https,
                       const KeyValMap* http_header_map, const KeyValMap* http_query_map, const char* data,
                       int data_len) override;
    void OnHttpPutReq(const ConnGuid* conn_guid, struct evhttp_request* evhttp_req, bool https,
                      const KeyValMap* http_header_map, const KeyValMap* http_query_map, const char* data,
                      int data_len) override;'''
            fp.write(content.encode('utf-8'))
        else:
            return -1

        content = [os.linesep, '};', os.linesep, namespace_end, os.linesep * 2,
                   '#endif // %s' % guard, os.linesep]
        fp.write(''.join(content).encode('utf-8'))

        return 0
    except Exception as e:
        print('exception: %s' % e)
        return -1


def output_header_file(msg, output_dir, namespace_list):
    for namespace in namespace_list:
        file_path = os.path.join(output_dir, namespace, name_style_util.camel_to_underline(msg).lower() + '_handler.h')
        file_util.del_file(file_path)
        file_util.make_dir(file_util.file_dir(file_path))

        try:
            fp = open(file_path, 'wb')

            output_header_file_content(fp, msg, namespace)
            fp.close()

            print('=== generate %s done ===' % file_path)
        except Exception as e:
            print('exception: %s' % e)
            return -1

    return 0


def output_cpp_file_content(fp, msg, pkg_name, namespace):
    try:
        if 'proto_tcp' == namespace:
            namespace_begin = 'namespace tcp%s{%snamespace proto%s{' % (os.linesep, os.linesep, os.linesep)
            namespace_end = '}%s}' % os.linesep

        class_name = '%sHandler' % msg

        content = ['#include "%s_handler.h"' % name_style_util.camel_to_underline(msg).lower(),
                   '''
#include "cs_msg.pb.h"
#include "cs_msg_id.pb.h"
#include "err_code.h"''', os.linesep,
                   '#include "%s_protobuf_util.h"' % namespace, os.linesep * 2,
                   'using namespace %s;' % pkg_name, os.linesep * 2,
                   '%s' % namespace_begin, os.linesep,
                   '%s::%s()' % (class_name, class_name), os.linesep, '{', os.linesep, '}', os.linesep * 2,
                   '%s::~%s()' % (class_name, class_name), os.linesep, '{', os.linesep, '}', os.linesep * 2]

        if namespace == 'http':
            content.insert(1, '''
#include "evhttp.h"
#include "json/json.h"''')
            content.insert(6, '#include "http_conn_center_interface.h"%s' % (os.linesep * 2))

        fp.write(''.join(content).encode('utf-8'))

        if namespace == 'proto_tcp':
            req_msg_name = name_style_util.camel_to_underline(msg).lower()
            rsp_msg_name = name_style_util.camel_to_underline(msg).lower().replace('req', 'rsp')

            content = ['::proto::MsgID %s::GetMsgID()' % class_name, os.linesep, '{', os.linesep,
                       '    return cs::MSG_ID_%s;' % (req_msg_name.upper()), os.linesep,
                       '}', os.linesep * 2,
                       'void %s::OnMsg(const ConnGUID* conn_guid, const ::proto::MsgHead& msg_head, const void* msg_body, size_t msg_body_len)' % class_name,
                       os.linesep,
                       '{', os.linesep,
                       '    LOG_TRACE("%s::OnMsg");' % class_name, os.linesep * 2,
                       '    cs::%s %s;' % (msg, req_msg_name), os.linesep,
                       '    if (ParseProtobufMsg(&%s, msg_body, msg_body_len) != 0)' % req_msg_name, os.linesep,
                       '    {', os.linesep,
                       '        LOG_ERROR("failed to parse msg, msg id: " << msg_head.msg_id << ", msg body len: " << msg_body_len);',
                       os.linesep,
                       '        SendErrRsp(conn_guid, msg_head, ERR_INVALID_PARAM);', os.linesep,
                       '        return;', os.linesep,
                       '    }', os.linesep * 2,
                       '    // TODO', os.linesep * 2,
                       '    ////////////////////////////////////////////////////////////////////////////////',
                       os.linesep,
                       '    ::proto::MsgHead rsp_msg_head = msg_head;', os.linesep,
                       '    rsp_msg_head.msg_id = cs::MSG_ID_%s;' % rsp_msg_name.upper(), os.linesep * 2,
                       '    cs::%s %s;' % (msg.replace('Req', 'Rsp'), rsp_msg_name), os.linesep,
                       '    %s.mutable_err_ctx()->set_err_code(ERR_OK);' % rsp_msg_name, os.linesep * 2,
                       '    if (SendToClient(logic_ctx_->scheduler, conn_guid, rsp_msg_head, &%s) != 0)' % rsp_msg_name,
                       os.linesep,
                       '    {', os.linesep,
                       '        LOG_ERROR("failed to send to " << conn_guid << ", msg id: " << rsp_msg_head.msg_id);',
                       os.linesep,
                       '        return;', os.linesep,
                       '    }', os.linesep,
                       '}', os.linesep * 2,
                       'void %sHandler::SendErrRsp(const ConnGUID* conn_guid, const ::proto::MsgHead& req_msg_head, int err_code) const' % msg,
                       os.linesep, '{', os.linesep,
                       '    ::proto::MsgHead rsp_msg_head = req_msg_head;', os.linesep,
                       '    rsp_msg_head.msg_id = cs::MSG_ID_%s;' % rsp_msg_name.upper(), os.linesep * 2,
                       '    cs::%s %s;' % (msg.replace('Req', 'Rsp'), rsp_msg_name), os.linesep,
                       '    %s.mutable_err_ctx()->set_err_code(err_code);' % rsp_msg_name, os.linesep * 2,
                       '    SendToClient(logic_ctx_->scheduler, conn_guid, rsp_msg_head, &%s);' % rsp_msg_name,
                       os.linesep,
                       '}', os.linesep]
            fp.write(''.join(content).encode('utf-8'))
        elif namespace == 'http':
            content = ['const char* %s::GetHttpReqPath()' % class_name, os.linesep, '{', os.linesep,
                       '    return "/%s"' % name_style_util.camel_to_underline(msg).lower(), os.linesep,
                       '}', os.linesep * 2,
                       'void %s::OnHttpHeadReq(const ConnGuid* conn_guid, struct evhttp_request* evhttp_req, bool https, const KeyValMap* http_header_map, const KeyValMap* http_query_map)' % class_name,
                       os.linesep, '{', os.linesep, '}', os.linesep * 2,
                       'void %s::OnHttpGetReq(const ConnGuid* conn_guid, struct evhttp_request* evhttp_req, bool https, const KeyValMap* http_header_map, const KeyValMap* http_query_map)' % class_name,
                       os.linesep, '{', os.linesep, '}', os.linesep * 2,
                       'void %s::OnHttpPostReq(const ConnGuid* conn_guid, struct evhttp_request* evhttp_req, bool https, const KeyValMap* http_header_map, const KeyValMap* http_query_map, const char* data, int data_len)' % class_name,
                       os.linesep, '{', os.linesep, '}', os.linesep * 2,
                       'void %s::OnHttpPutReq(const ConnGuid* conn_guid, struct evhttp_request* evhttp_req, bool https, const KeyValMap* http_header_map, const KeyValMap* http_query_map, const char* data, int data_len)' % class_name,
                       os.linesep, '{', os.linesep, '}', os.linesep]
            fp.write(''.join(content).encode('utf-8'))
        else:
            return -1

        content = [namespace_end, os.linesep]
        fp.write(''.join(content).encode('utf-8'))

        return 0
    except Exception as e:
        print('exception: %s' % e)
        return -1


def output_cpp_file(msg, output_dir, pkg_name, namespace_list):
    for namespace in namespace_list:
        file_path = os.path.join(output_dir, namespace,
                                 name_style_util.camel_to_underline(msg).lower() + '_handler.cpp')
        file_util.del_file(file_path)
        file_util.make_dir(file_util.file_dir(file_path))

        try:
            fp = open(file_path, 'wb')
            cpp_pkg_name_list = pkg_name.split('.')

            output_cpp_file_content(fp, msg, '::'.join(cpp_pkg_name_list[:len(cpp_pkg_name_list) - 1]), namespace)
            fp.close()

            print('=== generate %s done ===' % file_path)
        except Exception as e:
            print('exception: %s' % e)
            return -1

    return 0


def output_csharp_file(msg, output_dir, pkg_name, namespace_list):
    pass


def generate_cpp_msg_handler_file(msg_proto_file, msg_list_group, output_dir, base_idx, gap, pkg_name, namespace_list):
    for msg_list in msg_list_group:
        if not msg_list or 0 == len(msg_list):
            continue

        for msg in msg_list:
            if msg.endswith('Req') or msg.endswith('Nfy'):
                if output_header_file(msg, output_dir, namespace_list) != 0:
                    return -1

                if output_cpp_file(msg, output_dir, pkg_name, namespace_list) != 0:
                    return -1
            else:
                output_csharp_file(msg, output_dir, pkg_name, namespace_list)

    return 0


def test_001():
    msg_list_group = []
    msg_mgr_ = one_file_msg_mgr.OneFileMsgMgr()

    msg_proto_file = 'demo_msg.proto'
    if msg_mgr_.read_msg(msg_proto_file) != 0:
        return -1

    msg_list_group.append(msg_mgr_.msg_list)

    if generate_cpp_msg_handler_file(msg_proto_file, msg_list_group, './output/demo', None, None,
                                     'com::moon::demo', ['proto_tcp', 'http']) != 0:
        return -1

    return 0


if __name__ == '__main__':
    test_001()
