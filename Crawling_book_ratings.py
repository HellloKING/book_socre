import csv
import requests
from bs4 import BeautifulSoup
data_list = []
login_url = 'https://wp.forchange.cn/wp-admin/admin-ajax.php'
username = input('请输入用户名:')
password = input('请输入密码:')
login_data = {
    'action':'ajaxlogin',
    'username':username,
    'password':password,
    'remember':'true'
}
login_res = requests.post(login_url,data=login_data)
for page in range(1,4):
    book_list_url = 'https://wp.forchange.cn/resources/page/{}/'.format(page)
    book_list_res = requests.get(book_list_url)
    soup = BeautifulSoup(book_list_res.text,'html.parser')
    book_href_lsit = soup.find_all('a',class_='post-title')
    for href in book_href_lsit:
        book_name = href.text
        book_url = href['href']
        comment_res = requests.get(book_url,login_res.cookies)
        soup = BeautifulSoup(comment_res.text,'html.parser')
        score_data = soup.find('div',id='curItemTotalStar')
        score = score_data.find('b')
        score_number = score_data.find('p',class_='wk')
        if score == None:
            score = '暂无评分'
        else:
            score = score.text
        if score_number == None:
            score_number = '暂无评分'
        else:
            score_number = score_number.text[7:-5]
        book_data = {
            '书籍名称':book_name,
            '书籍评分':score,
            '评分人数':score_number
        }
        print(book_data)
        data_list = data_list.append(book_data)
with open('E:\python\Python爬虫\爬取的信息\CSV/书籍评分.csv','w',encoding='utf-8-sig')as f:
    file_write = csv.DictWriter(f,fieldnames=['书籍名称','书籍评分','评分人数'])
    file_write.writeheader()
    file_write.writerows(data_list)