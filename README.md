# :ok_hand: is213-project :ok_hand:

# IS213 - Group 7 - TradingWheels :bike:

## Table of Contents
* [Group Members](#family-group-members)
* [Project Overview](#moneybag-project-overview-moneybag)
    * [Buy Stocks](#globe_with_meridians-buy-stocks)
    * [Sell Stocks](#star-sell-stocks)
    * [Stock Recommender](#dart-stock-recommender)
* [How to Use (for Visitors)](#question-how-to-use-our-web-application-for-visitors-to-our-website)
    * [Point to Note](#warning-point-to-note)
* [Others](#notebook_with_decorative_cover-others)

## :family: Group Members

| # | Name | SMU Email Address | Roles and Responsibilities |
| ----------- | ----------- | ----------- | ----------- |
| 1 | Caslyn Phang | caslynphang.2020@scis.smu.edu.sg | <ul><li></li></ul>|
| 2 | Teh Xue Er | xueer.teh.2020@scis.smu.edu.sg | <ul><li></li></ul>|
| 3 | Jethro Ong Yong En | jethro.ong.2020@scis.smu.edu.sg | <ul><li></li></ul>|
| 4 | Goh Soon Hao | soonhao.goh.2020@scis.smu.edu.sg |<ul><li></li></ul>|
| 5 | Teoh Chin Hao Jordan | jordan.teoh.2020@scis.smu.edu.sg | <ul><li></li></ul>|

## :moneybag: Project Overview :moneybag:
### Background
Trading Wheels is a paper trading microservice application that is used to educate beginner investors about the buying/ selling of financial instruments on the stock market.

<div align='center'>
    <h1 style="color: #6C5CE7">TradingWheels</h1>
    <img src="images/logo.png">
</div>

## :question: How to Use Our Web Application (for Visitors to our Website)

### :full_moon: General Overall Scenario: :full_moon:

1. Insert login.html into web root folder
2. Run "docker-compose up" in the folder that holds the docker-compose.yml file
3. Open up login.html in browser
4. Key in details to login if user has an account, or click sign up to sign up for new account
5. Once at home page, user will see the recommended stocks based on trade volume or they can choose to search for a particular stock to buy or sell

### :globe_with_meridians: Buy Stocks
6. User can search for the particular stock to buy
7. single_stock_view page will display the closing price of the day
8. User can click on the buy button, where the quantity to purchase will pop up
9. After placing the buy order, the User's portfolio will be updated
10. When the portfolio is successfully updated, notification of successful purchase will be sent

### :star: Sell Stocks
6. User can search for the particular stock to buy
7. single_stock_view page will display the closing price of the day
8. User can click on the sell button, where the quantity to sell will pop up
9. After placing the sell order, the User's portfolio will be updated
10. When the portfolio is successfully updated, notification of successful sale will be sent

### :dart: Stock Recommender
6. User clicks on stocks recommended based on the last transacted stock price
7. single_stock_view page will display recommended stock chosen

### :warning: Point to note

The database is only found locally, thus importing the sql file would be required to load and store the data. Additional features such as a cloud database etc were not done due to time constraints. For testing purposes, you can access the website on localhost and follow the instructions below.

## :notebook_with_decorative_cover: Others

How to link - [Google Login](https://developers.google.com/identity/gsi/web)

How to add image - ![Logo](images/logo.png)

