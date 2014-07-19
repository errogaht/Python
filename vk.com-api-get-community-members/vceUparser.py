# -*- coding: utf-8 -*-


import wx
import requests
import json
import threading


def CommunityExtractIds(id):
    params = {'group_id': id, 'sort': 'id_asc', 'offset': '0', 'count': '1000'}
    r = requests.get("http://api.vk.com/method/groups.getMembers", params=params)
    jsonData = r.text
    jsonData = json.loads(jsonData)
    count = jsonData['response']['count']
    outList = []  # создаём пустой список
    outList.extend(jsonData['response']['users'])
    if count > 1000:
        offset = 1000
        while offset < count:
            params.update({'offset': offset})
            r = requests.get("http://api.vk.com/method/groups.getMembers", params=params)
            jsonData = r.text
            jsonData = json.loads(jsonData)
            outList.extend(jsonData['response']['users'])
            offset = len(outList)

    # запишем строку в файл
    uIdOut = ''
    for uId in outList:
        uIdOut = uIdOut + str(uId) + '\n'
    f = open('out/' + id + '.txt', 'w')
    f.write(str(uIdOut))
    f.close()
    print(str(count) + ' ID экспортированны из ' + str(id))

app = wx.App()
wnd = wx.Frame(None, wx.ID_ANY, "I'm the title")
b = wx.Button(wnd, -1, "Create and Show a TextEntryDialog", (50, 50))
wnd.Show(True)
while 1:
    dlg = wx.TextEntryDialog(wnd, 'What is your favorite programming language?', 'Eh??', 'Python')
    dlg.SetValue("6885780")
    if dlg.ShowModal() == wx.ID_OK:
        id = dlg.GetValue()
        p1 = threading.Thread(target=CommunityExtractIds, name=id, args=[id])
        p1.start()
    else:
        if dlg.ShowModal() == wx.ID_CANCEL:
            app.Destroy()

dlg.Destroy()
app.MainLoop()


raw_input(input)

