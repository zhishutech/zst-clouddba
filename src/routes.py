
from handlers.mysqlcnf_handler import GenMysqlcnfHandler
from handlers.snapshot_handler import UploadSnapshotHandler


handlers = [
    (r"/api/v1/mysqlcnf/gen", GenMysqlcnfHandler),
    (r"/api/v1/snapshot/upload", UploadSnapshotHandler),
    #(r"/api/v1/mysql/Inspection", MysqlInspectionHandler), 
]