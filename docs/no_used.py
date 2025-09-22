        #         li = xbmcgui.ListItem(label=meta["title"])
        #         # 获取 Video InfoTag 对象
        #         info_tag = li.getVideoInfoTag()
        #         info_tag.setTitle(meta["title"])
        #         info_tag.setPlot(meta["plot"])
        #         if meta["trailer"] and os.path.exists(meta["trailer"]):
        #             li.setProperty("IsPlayable", "true")
        #             info_tag.setTrailer(meta["trailer"])
        #             self.log(f"--- Trailer found for {meta['title']} {meta['trailer']} ---", level=xbmc.LOGINFO)
        #         else:
        #             self.log(f"No trailer found for {meta['title']} {meta['trailer']}", level=xbmc.LOGINFO)
        #         if meta["thumb"] and os.path.exists(meta["thumb"]):
        #             li.setArt({
        #                 "thumb": meta["thumb"],
        #                 "poster": meta["thumb"],
        #                 "fanart": meta["thumb"]
        #             })
        #         else:
        #             self.log(f"No thumb found for {meta['title']} {meta['thumb']}", level=xbmc.LOGINFO)


        #         # ✅ 关键修改：不直接播放 ROM，而是绑定一个 “虚拟 URL” 用于点击后触发 RetroPlayer
        #         # 使用 plugin:// 协议构造一个“跳转指令”，避免 Kodi 尝试解码 .nes
        #         play_url = f"{self.base_url}?play={rom_path}&title={meta['title']}"

        #         xbmcplugin.addDirectoryItem(
        #             handle=self.handle,
        #             url=play_url,
        #             listitem=li,
        #             isFolder=False
        #         )
        # xbmcplugin.setContent(self.handle, 'movies')
        # # viewmode 可选枚举值：https://telaak.github.io/kodi-jsonrpc-api/types/ViewMode.html
        # xbmc.executebuiltin('Container.SetViewMode("list")')
        # xbmcplugin.endOfDirectory(self.handle)


    def list_games_in_directory(self, directory):
        xml_file = os.path.join(directory, "gamelist.xml")
        self.log(f"xml file in directory: {xml_file}", level=xbmc.LOGINFO)
        game_info = {}

        if os.path.exists(xml_file):
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                for g in root.findall("game"):
                    fname = g.findtext("path")
                    self.log(f"Found ROM config: {fname}", level=xbmc.LOGINFO)
                    if not fname:  # 如果没有 path 属性，跳过这条记录
                        continue
                    title = g.findtext("name", fname)
                    plot = g.findtext("desc", "")
                    thumb = g.findtext("image", "")
                    trailer = g.findtext("video", "")
                    if thumb:
                        thumb = os.path.normpath(os.path.join(directory, thumb))
                        if not os.path.exists(thumb):
                            thumb = None
                    if trailer:
                        trailer = os.path.normpath(os.path.join(directory, trailer))
                        if not os.path.exists(trailer):
                            trailer = None
                    if fname.startswith("./"):
                        fname = fname[2:]  # 去掉前两个字符
                    
                    rom_path = os.path.normpath(os.path.join(directory, fname))
                    if not os.path.exists(rom_path):
                        continue
                    game_info[fname] = {
                        "path": rom_path,
                        "title": title,
                        "plot": plot,
                        "thumb": thumb,
                        "trailer": trailer
                    }
                self.log(f"Found ROM list: {game_info}", level=xbmc.LOGINFO)
            except Exception as e:
                self.log(f"parse xml file error: {e}", level=xbmc.LOGWARNING)
                parse_error = self.addon.getLocalizedString(30302)
                xbmcgui.Dialog().notification(parse_error, str(e))
        else:
            # 渲染子目录
            for subdir in os.listdir(directory):
                li = xbmcgui.ListItem(label=subdir)
                url = f"{self.base_url}?dir={urllib.parse.quote_plus(os.path.join(directory, subdir))}"
                xbmcplugin.addDirectoryItem(self.handle, url, li, isFolder=True)
            xbmcplugin.endOfDirectory(self.handle)
            return
        file_list = os.listdir(directory)
        sort_file_list = sorted(file_list)
        for file in sort_file_list:
            if file.endswith(ROM_EXTENSIONS):
                rom_path = os.path.join(directory, file)
                # self.log(f"Found ROM file: {file}", level=xbmc.LOGINFO)
                meta = game_info.get(file)
                if not meta:
                    meta = {"title": file, "plot": "", "thumb": "", "trailer": "", "path": rom_path}
                game_info[file] = meta
                # self.log(f"Found meta file: {meta}", level=xbmc.LOGINFO)
        # ✅ 关键修复：清空窗口残留状态
        # xbmc.executebuiltin("Container.Update(plugin://plugin.video.game-visuals/, replace)")
        # ✅ 唤起自定义窗口
        try:
            w = MyWindow(
                "mywindow.xml",
                self.addon.getAddonInfo("path"),
                "default",
                "720p",
                items=list(game_info.values()),
                base_url=self.base_url,
                handle=self.handle
            )
            w.show()
            del w
        except Exception as e:
            self.log(f"Error showing window: {e}", level=xbmc.LOGWARNING)

