import requests
from bs4 import BeautifulSoup
from csv import writer

# response = requests.get('https://search.bilibili.com/all?keyword=%E3%82%A2%E3%83%8B%E3%82%B2%E3%83%A9%EF%BC%81%E3%83%87%E3%82%A3%E3%83%89%E3%82%A5%E3%83%BC%E3%83%BC%E3%83%B3')
#
# soup = BeautifulSoup(response.text, 'html.parser')
#
#
#
# with open("videoLinks.csv", 'w') as csv_file:
#     csv_writer = writer(csv_file)
#     header = ['URLS']
#     csv_writer.writerow(header)
#
#     for video in soup.find_all('a', class_='img-anchor'):
#         link = video['href'].replace('//','')
#         csv_writer.writerow([link])



###Version 2
# response = requests.get('https://search.bilibili.com/all?keyword=%E3%82%A2%E3%83%8B%E3%82%B2%E3%83%A9%EF%BC%81%E3%83%87%E3%82%A3%E3%83%89%E3%82%A5%E3%83%BC%E3%83%BC%E3%83%B3')

# soup = BeautifulSoup(response.text, 'html.parser')
# videos = soup.find_all(class_='video-item matrix')


# with open("videoLinks.csv", 'w') as csv_file:
#     csv_writer = writer(csv_file)
#     header = ['URLS']
#     csv_writer.writerow(header)

#     for video in videos.find_all('a'):
#         link = video.get('href').replace('//','')
#         csv_writer.writerow([link])





response = requests.get('https://space.bilibili.com/1726310/video')

soup = BeautifulSoup(response.text, 'html.parser')


with open("videoLinksCharm.csv", 'w') as csv_file:
    csv_writer = writer(csv_file)
    header = ['URLS']
    csv_writer.writerow(header)

    for video in soup.find_all('a', class_='cover'):
        link = video['href'].replace('//', '')
        csv_writer.writerow([link])
