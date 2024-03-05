import requests

apiheaders = {"Client-id":"0pk5p1k5yckbh687emzecmb1qljuqo","Authorization": "Bearer 36ru0itu7fgwv6nc5d8a872jbt3bam"}

while True:

  entry =  input('* 스트리머 찾기 : ')
  userlogin = entry[entry.rfind('/')+1:]
  req = requests.get(f'https://api.twitch.tv/helix/users',{'login':userlogin},headers=apiheaders)
  userid = req.json()['data'][0]['id']
  print(f"- 유저 조회하는 중 ({userlogin})")

  after = None
  follow = []
  while True:
    req = requests.get(f'https://api.twitch.tv/helix/users/follows',{'from_id':userid,'first':100,'after':after},headers=apiheaders)
    if not req.json()['data']:
      break
    follow.extend(map(lambda x:x['to_login'],req.json()['data']))
    print(f"- 팔로우 목록 조회하는 중 ({len(follow)}/{req.json()['total']})")
    if not req.json()['pagination']:
      break
    after = req.json()['pagination']['cursor']

  stream = []
  for i in range(0,len(follow),100):
    req = requests.get('https://api.twitch.tv/helix/streams',{'user_login':follow[i:i+100]},headers=apiheaders)
    stream.extend(map(lambda x:x,req.json()['data']))
    print(f"- 스트림 목록 조회하는 중 ({len(stream)})")

  ward = []
  for n,i in enumerate(stream,1):
    req = requests.get(f"https://tmi.twitch.tv/group/user/{i['user_login']}/chatters")
    if userlogin in sum(req.json()['chatters'].values(),[]):
      print(f"- 채팅창 조회하는 중 ({n}/{len(stream)}) → {i['user_login']} 채널에서 발견됨")
      ward.append(i)
    else:
      print(f"- 채팅창 조회하는 중 ({n}/{len(stream)})")

  for n,i in enumerate(ward,1):
    print(f"- [{n}] {i['user_name']} (https://www.twitch.tv/{i['user_login']})")
  print()