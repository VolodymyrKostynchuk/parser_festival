from bs4 import BeautifulSoup

import requests
import lxml
import json


def get_data():
	count = 1 
	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
	}

	fest_urls_list = []
	fest_finish_data = {}

	for i in range(0, 288, 24):
		url = f'https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=&from_date=24%20Apr%202022&to_date=&maxprice=500&o={i}&bannertitle=May'

		req = requests.get(url, headers=headers)
		json_data = json.loads(req.text)
		html_response = json_data['html']

		# with open(f'data\\index_{i}.html', 'w', encoding='utf-8') as f:
		# 	f.write(html_response)

		with open(f'data\\index_{i}.html', encoding='utf-8') as f:
			src = f.read()

		soup = BeautifulSoup(src, 'lxml')
		cards = soup.find_all('a', class_='card-img-link')

		for i in cards:
			fest_url = 'https://www.skiddle.com/' + i.get('href')
			fest_urls_list.append(fest_url)


	for url in fest_urls_list:
		
		req = requests.get(url, headers=headers)
		src = req.text
		soup = BeautifulSoup(src, 'lxml')

		fest_name = soup.find('h1').text.strip()
		fest_data = soup.find('h3').text.strip()
		fest_locations_url = 'https://www.skiddle.com/' + soup.find('a', class_='tc-white').get('href')

		try:
			req = requests.get(fest_locations_url, headers=headers)
			src = req.text
			soup = BeautifulSoup(src, 'lxml')

			contacts = soup.find('h2', string='Venue contact details and info').find_next()
			items = [item.text for item in contacts.find_all('p')]

			contacts_dict = {}

			for cd in items:
				contact_list = cd.split(':')

				if len(contact_list) == 3:
					contacts_dict[contact_list[0].strip()] = contact_list[1].strip() + ':' + contact_list[2].strip()

				else:
					contacts_dict[contact_list[0].strip()] = contact_list[1].strip()

			fest_finish_data = {
				'Fest_name': fest_name,
				'Fest_data': fest_data,
				'Fest_locations': fest_locations_url,
				'Contact': contacts_dict,
			}



			with open('data\\json_data\\project_data.json', 'a', encoding='utf-8') as f:
				json.dump(fest_finish_data, f, indent=4, ensure_ascii=False)
			
			print('#' * 10)
			print(f'{count} of 264')
			count += 1 

		except Exception as ex:
			print(f'{ex}')


def main():
	get_data()


if __name__ == '__main__':
	main()