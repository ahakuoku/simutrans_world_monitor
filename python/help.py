# -*- coding: utf-8 -*- 
# ヘルプなど

import discord

helps = {}

helps['?help'] = discord.Embed(title="コマンド一覧", description="本botで使用できるコマンドは次の通りです。\n※helpコマンド・ipコマンド・aboutコマンド以外はSimutrans起動時以外使用できません。\n引数の区切りはコンマ(`,`)で行います。\n`<>`のカッコ内は、その引数が必須であることを示します。（カッコは外してください）\n`[]`のカッコ内は、その引数がオプションであることを示します。（カッコは外してください）", color=0x00ff00)
helps['?help'].add_field(name="`?help`", value="本botのヘルプを返します。", inline=False)
helps['?help'].add_field(name="`?wait,<駅名>,[エントリ数]`", value="指定された停車場の待機客およびその行き先を返します。エントリ数のデフォルト値は5です。", inline=False)
helps['?help'].add_field(name="`?player`", value="ゲームに参加している会社一覧と、その番号を返します。ここで返される番号は、プレイヤー番号を指定するコマンドで使用します。", inline=False)
helps['?help'].add_field(name="`?akabo,[プレイヤー番号]`", value="指定した会社に所属する停車場で、いわゆる赤棒が立っている駅とその待機客を返します。プレイヤー番号の指定がない場合は、すべての会社の赤棒を返します。", inline=False)
helps['?help'].add_field(name="`?time`", value="現在の年と月を返します。", inline=False)
helps['?help'].add_field(name="`?finance`", value="各会社の資金を返します。", inline=False)
helps['?help'].add_field(name="`?route,<プレイヤー番号>,[路線属性]`", value="指定したプレイヤーの路線番号と路線名を一覧で返します。", inline=False)
helps['?help'].add_field(name="`?halt,<路線番号>,[停車場数]`", value="指定した路線のスケジュール上にある停車駅を順番に返します。3つ目のパラメーターを指定すると、路線上にある駅を利用者順でソートして返します。", inline=False)
helps['?help'].add_field(name="`?convoy,<プレイヤー番号>,[編成属性]`", value="指定したプレイヤーの編成番号と編成名を一覧で返します。", inline=False)
helps['?help'].add_field(name="`?ip`", value="接続先を返します。", inline=False)
helps['?help'].add_field(name="`?about`", value="このBotの概要を返します。", inline=False)

helps['?接続先'] = discord.Embed(title="接続先情報", description="ahns.simutrans.info:65535", color=0x00ff00)
helps['?接続先'].set_footer(text="2021年12月現在")
helps['?address'] = discord.Embed(title="接続先情報", description="ahns.simutrans.info:65535", color=0x00ff00)
helps['?address'].set_footer(text="2021年12月現在")
helps['?ip'] = discord.Embed(title="接続先情報", description="ahns.simutrans.info:65535", color=0x00ff00)
helps['?ip'].set_footer(text="2021年12月現在")

helps['?about'] = discord.Embed(title="このBotについて", description="このBotは、Discord上でゲーム内の様々な情報を提供するbotです。\n\nこのBotは、Simutrans world monitor( <https://github.com/teamhimeh/simutrans_world_monitor/blob/main/README.md> )をカスタマイズしたものを使用しています。\n仕様の詳細は`?help`と入力してください。ソースコードはGitHub( <https://github.com/ahakuoku/simutrans_world_monitor/tree/knAHNS_deleted> )をご覧ください。", color=0x00ff00)