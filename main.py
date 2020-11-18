# ---------目录结构--------- #
# 项目文件夹
# static
# city
# city_Name
# Img
# Video
# describe,json
# ---------目录结构--------- #


# ---------外部依赖--------- #
from flask import Flask, render_template, send_file, redirect, url_for, request
# ***表单*** #
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, DataRequired
from wtforms import StringField, SubmitField, FloatField
from flask_bootstrap import Bootstrap

import os
import json
import random
from gevent import pywsgi

# ---------外部依赖--------- #


# ------------flask初始化------------ #
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
bootstrap = Bootstrap(app)
# ------------flask初始化------------ #


# ------------具名常量------------ #
Root = 'static/city'  # 存放城市文件夹的目录
Belo = ['Img', 'Video']


# ------------具名常量------------ #


# -------------全局函数------------- #
# 返回不含后缀的文件路径
def getRoute(No, Belong, MyCityName):
    return Root + '/' + MyCityName + '/' + Belo[Belong] + '/' + No


# 返回包含所有城市名的list
def getCityList():
    list = []
    for dir in os.listdir(Root):
        if not os.path.isfile(Root + '/' + dir):
            if os.path.exists(Root + '/' + dir + '/' + 'describe.json'):
                list.append(dir)

    return list


# -------------全局函数------------- #

# -------------类------------- #
# ***资产管理类*** #
# 一个City包含一个asset，专门管理图像和视频
class asset:
    Info = None
    Belong = -1
    No = -1
    city_name = ''

    def __init__(self, belong, no, city_name):
        # print("%%%%%%%%%%%%%%%%%%%%%%\n")
        # print(city_name)
        # print("%%%%%%%%%%%%%%%%%%%%%%\n")
        jroute = getRoute(no, belong, city_name) + '.json'
        f = open(jroute, encoding='utf-8')

        self.Info = json.load(f)
        self.city_name = city_name
        self.Belong = belong
        self.No = no

    def getVedioPath(self):
        path = getRoute(self.No, self.Belong, self.city_name)
        if os.path.exists(path + '.mp4'):
            return path + '.mp4'
        return None

    def getImgPath(self):
        path = getRoute(self.No, self.Belong, self.city_name)
        Types = ['.png', '.jpeg', '.jpg', '.jfif']
        for T in Types:
            if os.path.exists(path + T):
                return path + T
        return None

    def getPath_JPG(self):
        if (Belo[self.Belong] != 'Img'):
            return None
        path = getRoute(self.No, self.Belong, self.city_name) + '.jpg'
        if os.path.exists(path):
            return path
        else:
            path = getRoute(self.No, self.Belong, self.city_name) + '.jpeg'
            if os.path.exists(path):
                return path
            return None

    def getTheme(self):
        return self.Info['theme']

    def getTitle(self):
        return self.Info['title']

    def getDescribe(self):
        return self.Info['describe']

    def getLocation(self):
        return self.Info['location']

    def getYear(self):
        return self.Info['year']

    def getMonth(self):
        return self.Info['month']

    def getSource(self):
        return self.Info['source']


# ***城市类*** #
# 一个网页只创建一个实例，提供访问各种信息的接口
class city:
    CityName = None
    Info = None
    Imgs = []
    Videos = []

    def GetAssetsList(self, List, Belong):
        List.clear()
        for file in os.listdir(Root + '/' + self.CityName + '/' + Belo[Belong]):
            if (file.endswith('.json')):
                Tmp = asset(Belong, file.rsplit('.', 1)[0], self.CityName)  # 后向分割去扩展名
                List.append(Tmp)

    def __init__(self, cityName):
        self.CityName = cityName
        jroute = Root + '/' + cityName + '/' + 'describe.json'
        f = open(jroute, encoding='utf-8')
        self.Info = json.load(f)
        self.GetAssetsList(self.Imgs, 0)
        self.GetAssetsList(self.Videos, 1)

    def GetImgPath(self):
        Types = ['.png', '.jpeg', '.jpg', '.jfif']
        for T in Types:
            path = Root + '/' + self.CityName + '/' + '000' + T
            if os.path.exists(path):
                return path

    def GetName(self):
        return self.CityName

    def GetDescribe(self):
        return self.Info["describe"]

    def GetTitle(self):
        return self.Info["title"]

    # 纬度
    def GetLatitude(self):
        return self.Info["latitude"]

    # 经度
    def GetLongitude(self):
        return self.Info["longitude"]


# ***简单城市类*** #
# 为检索提供信息
class simple_city:
    CityName = None
    Info = None

    def __init__(self, cityName):
        self.CityName = cityName
        jroute = Root + '/' + cityName + '/' + 'describe.json'
        f = open(jroute, encoding='utf-8')
        self.Info = json.load(f)

    def GetImgPath(self):
        Types = ['.png', '.jpeg', '.jpg', '.jfif']
        for T in Types:
            path = Root + '/' + self.CityName + '/' + '000' + T
            if os.path.exists(path):
                return path

    def GetName(self):
        return self.CityName

    def GetDescribe(self):
        return self.Info["describe"]

    def GetTitle(self):
        return self.Info["title"]

    # 纬度
    def GetLatitude(self):
        return self.Info["latitude"]

    # 经度
    def GetLongitude(self):
        return self.Info["longitude"]


class city_position:
    name = ''
    latitude = None
    longitude = None
    cssTop = None
    cssLeft = None

    def __init__(self, cityName):
        self.name = cityName
        jroute = Root + '/' + cityName + '/' + 'describe.json'
        f = open(jroute, encoding='utf-8')
        cityInfo = json.load(f)
        self.latitude = cityInfo["latitude"]
        self.longitude = cityInfo["longitude"]
        self.calculatePosition()

    def calculatePosition(self):
        a = 1.1325
        b = -62.6024
        c = -2.8505
        d = 147.271
        ImgWidth = 6
        self.cssLeft = a * self.longitude + b -ImgWidth/2
        self.cssTop = c * self.latitude + d

    def getCSSLeft(self):
        return self.cssLeft

    def getCSSTop(self):
        return self.cssTop

    def getName(self):
        return self.name

    def getURL(self):
        return '/city.'+ self.name


# ***表单类*** #
# 新建城市
class addCityForm(FlaskForm):
    name = StringField('CityName', validators=[DataRequired()])
    img = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['png','jpg'])])
    source = StringField('ImgSource')
    tags = StringField('Tags ( split by [,] )')
    title = StringField('Title')
    describe = StringField('Describe')


    # 经纬
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])

    submit = SubmitField("Submit")

    def getImg(self):
        return self.img.data

    def getTags(self):
        tagsStr = self.tags.data
        tagsList = tagsStr.split(',')
        return tagsList

    def getName(self):
        return self.name.data

    def getTitle(self):
        return self.title.data

    def getDescribe(self):
        return self.describe.data

    def getSource(self):
        return self.source.data

    def getLatitude(self):
        return self.latitude.data

    def getLongitude(self):
        return self.longitude.data

    def outPutToDisk(self):
        # 路径是否存在
        route = 'static/city/' + self.getName()

        ret = True
        if os.path.exists(route):
            route = 'static/upload/' + self.getName() + '_No.' + str(random.randint(0, 100000))
            ret = False

        os.makedirs(route)
        os.makedirs(route+"/img")
        os.makedirs(route+"/video")
        imgFile = self.getImg()
        imgFile.save(route + '/000.jpg')

        jsonData = {'tags': self.getTags(), 'title': self.getTitle(),
                    'describe': self.getDescribe(), 'source': self.getSource(),
                    'latitude': self.getLatitude(), 'longitude': self.getLongitude()}
        jsonFile = json.dumps(jsonData, indent=4)
        with open(route + '/describe.json', 'w') as json_file:
            json_file.write(jsonFile)
            json_file.close()

        return ret


# 添加资源
class addAssetForm(FlaskForm):
    name = StringField('CiryName', validators=[DataRequired()])
    asset = FileField('Upload Asset', validators=[FileRequired(), FileAllowed(['png', 'jpg', 'mp4'])])
    theme = StringField('Theme')
    title = StringField('Title')
    describe = StringField('Describe')
    source = StringField('ImgSource')

    location = StringField('Location')
    year = StringField('Year')
    month = StringField('Month')

    submit = SubmitField("Submit")

    def getAsset(self):
        return self.asset.data

    def getTheme(self):
        return self.theme.data

    def getName(self):
        return self.name.data

    def getTitle(self):
        return self.title.data

    def getDescribe(self):
        return self.describe.data

    def getSource(self):
        return self.source.data

    def getYear(self):
        return self.year.data

    def getMonth(self):
        return self.month.data

    def getLocation(self):
        return self.location.data

    def getNumber(self, type):
        if type == 'video':
            route = 'static/city/' + self.getName() + '/video'
        else:
            route = 'static/city/' + self.getName() + '/img'

        for i in range(1, 999):
            if i < 10:
                Number = '00' + str(i)
            elif i < 100:
                Number = '0' + str(i)
            else:
                Number = str(i)

            if not os.path.exists(route + '/' + Number + '.json'):
                return Number

    def outPutToDisk(self):
        # 路径是否存在
        route = 'static/city/' + self.getName()

        if not os.path.exists(route):
            return False

        # save asset
        assetFile = self.getAsset()
        if (assetFile.filename.endswith('.mp4')):
            route += '/video'
            Number = self.getNumber('video')
            assetFile.save(route + '/' + Number + '.mp4')
        else:
            route += '/img'
            Number = self.getNumber('img')
            assetFile.save(route + '/' + Number + '.jpg')

        # save json
        jsonData = {'theme': self.getTheme(), 'title': self.getTitle(),
                    'describe': self.getDescribe(), 'location': self.getLocation(),
                    'year': self.getYear(), 'month': self.getMonth()
            , 'source': self.getSource()}
        jsonFile = json.dumps(jsonData, indent=4)
        with open(route + '/' + Number + '.json', 'w') as json_file:
            json_file.write(jsonFile)
            json_file.close()

        return True


# -------------类------------- #


# -------------渲染网页------------- #
# ***城市呈现页面*** #
@app.route('/city.<CityName>')
def City(CityName):
    print("__________________________\n")
    MyCity = city(CityName)
    print(CityName)

    return render_template('City.html', City=MyCity)


# ***提交页面-新建城市*** #
@app.route('/addCity', methods=['GET', 'POST'])
def addCity():
    form = addCityForm()
    if form.validate_on_submit():
        ret = form.outPutToDisk()
        if ret:
            return '<h1>Thank you :)</h1>'
        else:
            return '<h1>Thank you :)</h1>' \
                   'The city you added already exists, we will consider updating the content'
    return render_template('addCIty.html', form=form)


# ***提交页面-添加资源*** #
@app.route('/addAsset', methods=['GET', 'POST'])
def addAsset():
    form = addAssetForm()
    if form.validate_on_submit():
        ret = form.outPutToDisk()
        if ret:
            return '<h1>Thank you :)</h1>'
        else:
            return '<h1>Sorry, The City Not Exists Yet</h1>' \
                   'Please Add City First'
    return render_template('addAsset.html', form=form)


# ***用户交互搜索界面*** #
@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        print('yes')
        describe = request.form['destination']
        scenery = request.form['room']
        food = request.form['adult']
        activity = request.form['children']
        departure = request.form['check-in'][3:6]
        back = request.form['check-out'][3:6]
        Spring = ['Apr', 'Feb', 'Mar']  # -----------根据日期得到季节-------------#
        Summer = ['Jul', 'May', 'Jun']
        Autumn = ['Agu', 'Sep', 'Oct']
        Winter = ['Nov', 'Dec', 'Jan']
        if departure in Spring:
            season = 'spring'
        elif departure in Summer:
            season = 'summer'
        elif departure in Autumn:
            season = 'autumn'
        else:
            season = 'winter'
        city_chosen = find_the_city(describe, scenery, food, activity, season)  # 返回city类列表，储存符合搜索条件的城市
        return render_template('choice.html', city=city_chosen)  # 渲染网页（展示搜索结果）
    else:
        return render_template('index.html')


def find_the_city(describe, scenery, food, activity, season):
    print(scenery, food, activity, season)
    city_list = []
    path_season = 'database_search/season/' + season + '/'
    path_activity = 'database_search/activity/' + activity + '/'  # 路径名称要修改！！！！！！！！！！！！！
    path_food = 'database_search/food/' + food + '/'
    path_scenery = 'database_search/scenery/' + scenery + '/'

    path = 'static/city'  # 获取所有城市的名称列表      这里的路径要修改！！！！！！！！！！！！！
    path_name = 'static/city/cityname'
    all_city = []
    for root, dirs, files in os.walk(path_name, topdown=False):
        for name in dirs:
            all_city.append(name)
    print(all_city)
    for city_name in all_city:  # 此处需要提前得到一个所有城市的名称列表
        feature = {'city_name': city_name, 'season': 0, 'food': 0, 'activity': 0, 'scenery': 0, 'count': 0}
        my_path = path_season + city_name + '.json'
        if os.path.exists(my_path):  # 在对应分类文件夹下寻找是否存在此城市的json文件若存在则表明该城市符合搜索条件
            feature['season'] = 1
        my_path = path_activity + city_name + '.json'
        if activity == 'all' or os.path.exists(my_path):
            feature['activity'] = 1
        my_path = path_food + city_name + '.json'
        if food == 'all' or os.path.exists(my_path):
            feature['food'] = 1
        my_path = path_scenery + city_name + '.json'
        if scenery == 'all' or os.path.exists(my_path):
            feature['culture'] = 1
        feature['count'] = feature['season'] + feature['activity'] + feature['food'] + feature['scenery']
        city_list.append(feature)
    new_list = sorted(city_list, key=lambda e: e.__getitem__('count'), reverse=True)  # 依据符合搜索条件的程度取前六个城市

    city_chosen = []
    for i in range(2):
        print(new_list[i]['city_name'] + str(new_list[i]['count']))
        MyCity = simple_city(new_list[i]['city_name'])
        city_chosen.append(MyCity)
    city_name = 'Deqing'
    MyCity7 = simple_city(city_name)
    city_chosen.append(MyCity7)
    city_name = 'Luzhou'
    MyCity1 = simple_city(city_name)
    city_chosen.append(MyCity1)
    city_name = 'Xiangshan'
    MyCity2 = simple_city(city_name)
    city_chosen.append(MyCity2)
    city_name = 'Deqing'
    MyCity3 = simple_city(city_name)
    city_chosen.append(MyCity3)
    city_name = 'Lishui'
    MyCity4 = simple_city(city_name)
    city_chosen.append(MyCity4)
    return city_chosen


# ***主页*** #
@app.route('/')
def index():
    cityList = getCityList()
    positionList = []
    for city in cityList:
        positionList.append(city_position(city))

    return render_template('main.html', cityList=positionList)


# -------------渲染网页------------- #
if __name__ == '__main__':
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()
    app.run()
