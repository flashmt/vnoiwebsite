$library_index_content = [
  'Algo', 'Cấu trúc dữ liệu', 'Đồ thị', 'Quy hoạch động',
]

$create_topic = 'Thêm bài mới'
$reply = 'Reply'
$edit = 'Edit'
$pin = 'Pin'
$unpin = 'Unpin'

$LIB = 'Thư viện'
$CTDL = 'Cấu trúc dữ liệu'
$PDS = 'Persistent Data Structures'

$breadcrumbs = {
  :index => [$LIB],
  :CTDL => [$LIB, $CTDL],
  :PDS => [$LIB, $CTDL, $PDS],
  :create => [$LIB, $CTDL, 'Create new topic'],
  :reply => [$LIB, $CTDL, $PDS, $reply],
  :edit => [$LIB, $CTDL, $PDS, $edit],
}
