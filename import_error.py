found profile at /home/nate/.mozilla/firefox/b3qojsad.zacks
---------------------------------------------------------------------------
IndexError                                Traceback (most recent call last)
/media/nate/nates/github/scrape_zacks/scrape_zacks.py in <module>
    283 if __name__ == "__main__":
    284     # TODO: scrape EPS estimates, sales estimates, zacks ranks for more stocks
--> 285     daily_updater()

/media/nate/nates/github/scrape_zacks/scrape_zacks.py in daily_updater()
    270             if is_trading_day and today_ny.hour >= 20:  # wait until after market after-hours close and hopefully data is updated
    271                 print('not up to date; downloading')
--> 272                 dl_all_data()
    273             elif not is_trading_day:
    274                 # will use last trading day as date

/media/nate/nates/github/scrape_zacks/scrape_zacks.py in dl_all_data()
    225 def dl_all_data():
    226     driver = setup_driver()
--> 227     login(driver)
    228     all_good = False
    229     while not all_good:

/media/nate/nates/github/scrape_zacks/scrape_zacks.py in login(driver)
    112     driver.find_element_by_link_text('Sign In').click()
    113     # for some reason there are multiple useraname/password fields
--> 114     driver.find_elements_by_id('username')[-1].send_keys(username)
    115     driver.find_elements_by_id('password')[-1].send_keys(password)
    116     # click the "Sign In" button

IndexError: list index out of range
