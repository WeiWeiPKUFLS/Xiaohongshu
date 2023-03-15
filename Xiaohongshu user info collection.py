import json

# load data from json file
with open('/Users/weiwei/Documents/Atian/Atian user info 15Mar23.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# open text file for writing
with open('/Users/weiwei/Documents/Atian/user info output.txt', 'w', encoding='utf-8') as f:
    nickname = data['data']['nickname']
    desc = data['data']['desc']
    ip_location = data['data']['ip_location']
    tags = data['data']['tags']
    tags_name_type = ", ".join([f"{tag['name']}({tag['tag_type']})" for tag in tags])
    note_num_stat = {"posted": data['data']['note_num_stat']['posted'], "liked": data['data']['note_num_stat']['liked'], "collected": data['data']['note_num_stat']['collected']}
    interactions_count = {"follows": data['data']['interactions'][0]['count'], "fans": data['data']['interactions'][1]['count'], "interaction": data['data']['interactions'][2]['count']}
    profile_link = data['data']['share_link']
    # write elements to text file
    f.write("nickname: {}\n".format(nickname))
    f.write("description: {}\n".format(desc))
    f.write("ip location: {}\n".format(ip_location))
    f.write("identity tags: {}\n".format(tags_name_type))
    f.write("note number statistics: posted: {}, liked: {}, collected: {}\n".format(note_num_stat['posted'], note_num_stat['liked'], note_num_stat['collected']))
    f.write("interaction statistics: follows: {}, followers: {}, likes and collects: {}\n".format(interactions_count['follows'], interactions_count['fans'], interactions_count['interaction']))
    f.write("profile link: {}\n".format(profile_link))
