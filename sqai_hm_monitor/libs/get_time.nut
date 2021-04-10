// メッセージ定義
local text_time = "現在の日付は%d年%d月です。"

class get_time_cmd {
  // 今の時間を返す
  function exec(str) {
    local time = world.get_time()
    local f = file(path_output,"w")
	  time.month += 1
    f.writestr(format(text_time, time.year, time.month))
    f.close() 
  }
}
