include("libs/monitoring_base")
include("libs/common")

// playerがnullのときは全てのplayerを検査対象とする．
function _get_overcrowded_halts(player, ratio) {
  local och = []
  foreach (h in halt_list_x()) {
    //なぜかinstanceの比較では==が通らない
    if(player==null || h.get_owner().get_name()==player.get_name()) {
      och.append(h)
    }
  }
  local r = ratio
  och = och.filter(@(i,h) h.get_waiting()[0]>h.get_capacity(good_desc_x.passenger)*r)
  return och
}

class get_overcrowded_cmd {
  function exec(str) {
    local player = get_player_from_num(str, 1)
    if(player==null) {
      return //エラーメッセージは既に吐かれている．
    }
    local f = file(path_output,"w")
    local params = split(str,",")
    local och = _get_overcrowded_halts(player,1)
    local out_str = ""
    if(och.len()==0) {
      out_str = player.get_name() + " の駅では混雑していません。"
    } else {
      out_str = player.get_name() + " の以下の駅が混雑しています。\n"
      foreach (h in och) {
        out_str += (h.get_name() + " ... " + h.get_waiting()[0].tostring() + "/" + h.get_capacity(good_desc_x.passenger).tostring() + "人\n")
      }
    }
    f.writestr(rstrip(out_str))
    f.close() 
  }
}


class chk_overcrowded_cmd extends monitoring_base_cmd {
  overcrowded_halts = []
  warning_ratio = 1.0
  
  constructor(freq, ratio) {
    monthly_check_time = freq
    warning_ratio = ratio
  }
  
  function do_check() {
    local och = _get_overcrowded_halts(null, warning_ratio)
    local prev_och = overcrowded_halts //ラムダ式のために必要
    // なぜかhalt_xのinstance比較がいつもfalseになるので，nameで比較する．
    // あたらしくovercrowdedになったhalt
    local new_och = och.filter(@(i,h) prev_och.filter(@(j,k) k.get_name()==h.get_name()).len()==0)
    overcrowded_halts = och //更新
    if(new_och.len()==0) {
      // 新しく混雑した駅はないので，終了．
      return
    }
    
    // プレイヤーごとにまとめる
    local player_new_och = get_player_list().map(@(p) [p, new_och.filter(@(i,h) p.get_name()==h.get_owner().get_name())])
    local out_str = "【混雑情報】以下の駅が混雑しています。\n"
    foreach (pn in player_new_och) {
      if(pn[1].len()==0) {
        //この会社に混雑してる駅はない．
        continue
      }
      out_str += ("<" + pn[0].get_name() + ">\n")
      foreach (h in pn[1]) {
        out_str += (h.get_name() + " ... " + h.get_waiting()[0].tostring() + "/" + h.get_capacity(good_desc_x.passenger).tostring() + "人\n")
      }
    }
    
    local f = file(path_output,"w")
    f.writestr(rstrip(out_str))
    f.close()
  }
}
