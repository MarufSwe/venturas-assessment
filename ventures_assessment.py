import csv
from requests_html import HTMLSession

# Save file as CSV Format
csv_file = open('assessment_results.csv', 'w') #file name
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Categories', 'Image URL', 'Category', 'Product Name', 'Price', 'Available Size', 'Sense of size', 'Sence of size', 'Title of Description', 'General Description', 'Itemization', 'KW']) #column name

session = HTMLSession()
ALL_ITEM = []

def get_item_detail(url):
    if url is not None:
        item_detail= session.get(url)

        categories = item_detail.html.find('.breadcrumbList', first=True).text
        # print('categories: ', '\n', categories, '\n')

        im = ''
        image_url = item_detail.html.find('.main_image', first=False)
        for iu in image_url:
            img_url = 'https://shop.adidas.jp/'+ iu.attrs['src']
            im = img_url
            # print('image url: ', '\n', img_url, '\n')

        category = item_detail.html.find('.categoryName', first=True).text
        # print('category: ', '\n', category, '\n')

        product_name = item_detail.html.find('.itemTitle', first=True).text
        # print('product name: ', '\n', product_name, '\n')

        price = item_detail.html.find('.price-text', first=True).text
        # print('price: ', '\n', price, '\n')

        avl_size = ''
        available_size = item_detail.html.find('.test-sizeSelector > ul > li')
        for available in available_size:
            avl_size = available.text
            # print('available_size: ','\n', available.text, '\n')

        sense_of_size = item_detail.html.find('.sizeFitBar', first=True)
        # print('sense of size label: ', '\n', sense_of_size, '\n')

        sos = ''
        bars = item_detail.html.find('.bar > ul > li')
        for bar in bars:
            sos = bar.text
            # print('sense of size bar: ', sos, '\n')

        # coordinate_product = r.html.find('.coordinate_item_tile')
        # print('coordinate_product: ', coordinate_product)
        # for co in coordinate_product:
        #     print('coordinate product: ', co.text, '\n')

        title_of_des = item_detail.html.find('.itemFeature', first=True).text
        # print('title of description: ', '\n', title_of_des, '\n')

        gen_des_of_product = item_detail.html.find('.commentItem-mainText', first=True).text
        # print('general description of product: ', '\n', gen_des_of_product, '\n')

        itemization = item_detail.html.find('.articleFeatures', first=True).text
        # print('itemization: ', '\n', itemization, '\n')

        ky = ''
        kws = item_detail.html.find('.category_link > .inner > a')
        for kw in kws:
            ky = kw.text
            # print('KeyWord: ', kw.text, end='')

        ALL_ITEM.append({
            "categories": categories, "im": im, "category": category, "product_name": product_name, "price": price,
            "avl_size": avl_size, "sense_of_size": sense_of_size, "sos": sos, "title_of_des": title_of_des,
            "gen_des_of_product": gen_des_of_product, "itemization": itemization, "ky": ky
        })
        print(ALL_ITEM)

        csv_writer.writerow([categories, im, category, product_name, price, avl_size, sense_of_size, sos, title_of_des, gen_des_of_product, itemization, ky])
        # csv_file.close()


def product_list():
    site_url = 'https://shop.adidas.jp/item/?gender=mens&category=footwear&group=sneakers'  #main url
    url = session.get(site_url)
    items = url.html.find('.articleDisplayCard-children > a')
    for item in items:
        item_details = item.attrs['href']
        links = 'https://shop.adidas.jp' + item_details # get individual item link
        get_item_detail(links)

product_list()
