// メッセージ定義
local text_title = "%s の%s編成一覧（計 %d 編成） \n" //%sは会社名、属性名。%dは編成数
local text_convoy = "%d : %s\n" //%dは番号， %sは編成名
local text_convoy_verbose = "\"%s\",\"%s\",%d,%d,%d\n" //%sは路線名、編成名。%dは(x, y, z)座標，
local text_no_convoys = "%s 管轄の編成はありません。" // %sは会社名
local text_no_convoys_with_waytype = "%s 管轄の路線属性 %s の編成はありません。" //%sは会社名、属性名
local text_invalid_waytype_title = "路線属性 %s は指定できません。" //%sは属性名
local text_invalid_waytype_desc = "指定可能な編成属性は次のとおりです。"

include("libs/common")
include("libs/embed_out")

local MAX_CONVOY_COUNT = 100000 // 無限ループ防止用

class get_convoys_cmd {
  wts = [["s", "自動車", wt_road], ["r", "鉄道", wt_rail], ["w", "船", wt_water], ["m", "ﾓﾉﾚｰﾙ", wt_monorail], ["g", "マグレブ", wt_maglev], ["t", "路面軌道", wt_tram], ["n", "ﾅﾛｰｹﾞｰｼﾞ", wt_narrowgauge], ["a", "航空", wt_air]]

  function get_waytype(param) {
    local wt = filter(wts, (@(wt) wt[0]==param))
    return wt.len()>0 ? wt[0] : null
  }

  // 路線の一覧を返す
  function exec(str) {
    local player = get_player_from_num(str, 1)
    if(player==null) {
      return //エラーメッセージは既に吐かれている．
    }

    // waytype指定を抽出する
    local waytype = null
    local params = split(str,",")
    if(params.len()>=3) {
      waytype = get_waytype(params[2])
      if(waytype==null) {
        embed_error(format(text_invalid_waytype_title, params[2]), text_invalid_waytype_desc, wts)
        return
      }
    }

    // 隠し機能(編成路線、位置出力)
    local output_verbose_flag = false
    if(params.len()>=4) {
      if(params[3].tolower()=="true") {
        output_verbose_flag = true
      }
    }

    local convoys_count = world.get_convoy_list().get_count()

    // 編成のidがわからないので，編成がすべて出現するまでイテレートする．
    local i = 0 // ループのインデックス
    local cnt = 0 // ヒットした編成数
    local wt_cnt = 0 // 条件にマッチした編成数
    local convoys_str = ""
    if(output_verbose_flag) {
      convoys_str = "line_name,convoy_name,posx,posy,posz\n"
    }
    while (cnt<convoys_count&&i<MAX_CONVOY_COUNT) {
      i++
      local convoy = convoy_x(i)
      if(!convoy.is_valid()) {
        continue
      }
      cnt += 1
      if(convoy.get_owner().get_name()!=player.get_name()) {
        continue
      }
      if(waytype==null || convoy.get_waytype()==waytype[2]) {
        if(output_verbose_flag) {
          local line = convoy.get_line()
          local pos = convoy.get_pos()
          if(line==null) {
            convoys_str += format(text_convoy_verbose, "", pos.x, pos.y, pos.z, convoy.get_name())
          } else {
            convoys_str += format(text_convoy_verbose, line.get_name(), convoy.get_name(), pos.x, pos.y, pos.z)
          }
        } else {
          convoys_str += format(text_convoy, i, convoy.get_name())
        }
        wt_cnt += 1
      }
    }

    local wt_name = waytype==null ? "" : waytype[1]
    local title = format(text_title, player.get_name(), wt_name, wt_cnt)
    if (wt_cnt==0) {
      if (waytype!=null) {
        embed_error(format(text_no_convoys_with_waytype,player.get_name(),wt_name))
      } else {
        embed_error(format(text_no_convoys,player.get_name()))
      }
    } else {
      embed_normal(title, rstrip(convoys_str))
    }
  }
}
