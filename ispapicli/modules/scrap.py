import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import os
import sys


class Scrap:
    def __init__(self, URL=''):
        self.gitHubURL = 'https://github.com/hexonet/hexonet-api-documentation/tree/master/API'
        # init app directories
        self.__initAppDirectories()

    def __initAppDirectories(self):
        '''
        Check whether the app is running from the editor or from an executable file

        Returns:
        --------
        Null
        '''
        if getattr(sys, 'frozen', False):
            self.absolute_dirpath = os.path.dirname(sys.executable)
        elif __file__:
            self.absolute_dirpath = os.path.dirname(__file__)

        self.command_path = os.path.join(self.absolute_dirpath, '../commands/')
        self.session_path = os.path.join(self.absolute_dirpath,
                                         '../config/session.json')

    # recursive function
    def __getURLs(self, urls):
        '''
        A recursive function that get all documentation page fro GitHub

        Returns:
        --------
        List: Allurls
        '''
        # urls to return
        Allurls = []
        # parse url
        try:
            for url in urls:
                if (self.__checkUrlType(url) == 'file'):
                    Allurls.append(url)
                    print('url found: ' + url)
                else:
                    # it is a directory
                    # get all links in this directory
                    newLinks = self.__getPageURLs(url)
                    # for each link, call it by the function itself
                    for newlink in newLinks:
                        Allurls.extend(self.__getURLs([newlink]))
            return Allurls
        except Exception as e:
            print("Network erros occured, some commands skipped: " + e)

    def __getPageURLs(self, url):
        '''
        Get urls from single page that leads to single documentation each

        Returns:
        --------
        List: urls

        '''
        urls = []
        page = requests.get(url)
        # get page download status, 200 is success
        statusCode = page.status_code
        if statusCode == 200:
            # get the page content
            src = page.content
            # parse HTML content, create bs4 object
            html = BeautifulSoup(src, 'html.parser')
            # get table body
            tbody = html.table.tbody
            # get tr
            rows = tbody.find_all('tr', attrs={'class': 'js-navigation-item'})
            for row in rows:
                # href = row.a['js-navigation-open']
                td = row.find('td', attrs={'class': 'content'})
                href = td.find('a', attrs={'class': 'js-navigation-open'})
                # add the url to the urls
                urlLink = 'https://github.com/' + href.get('href')
                urls.append(urlLink)
            # return urls
            return urls
        else:
            raise Exception("Page couldn't loaded. Status code: " +
                            str(statusCode))

    def __checkUrlType(self, url):
        '''
        Check the type of the url found, either file with documentation or a directory

        Returns:
        --------
        String: <>
        '''

        if url.endswith('.md'):
            return 'file'
        else:
            return 'directory'

    def __getParsedPage(self, url):
        '''
        Get HTML elements from a signle page

        Returns:
        --------
        Set: article, table

        '''
        try:
            page = requests.get(url)
            # get page download status, 200 is success
            statusCode = page.status_code
            # get the page content
            src = page.content
            # parse HTML content, create bs4 object
            html = BeautifulSoup(src, 'html.parser')
            # get only the command description element
            article = html.article
            # table of parametrs
            table = article.table
            return article, table
        except Exception:
            return "Couldn't parse page: " + url

    def __getCommandName(self, article):
        '''
        Return the h1 element in article block which is the command name

        Returns:
        --------
        String: commandName
        '''
        commandName = article.h1.text
        return commandName

    # description of the command
    def __getCommandDescription(self, article):
        '''
        Extract the command description

        Returns:
        --------
        String: desc | ''
        '''
        # adding exception for webely
        try:
            desc = article.find_all('p')
            return desc[0].text
        except Exception:
            return ' '

    # get comman avaiablity
    def __getCommandAvailability(self, article):
        '''
        Extract the 2nd p which is the availability

        Returns:
        --------
        String: ava | ' '
        '''
        try:
            ava = article.find_all('p')
            return ava[1].text
        except Exception:
            return ' '

    def __getCommandParameters(self, table):
        '''
        Extract the params from the command description table

        Returns:
        --------
        List: params
        '''
        headers = self.__getTableHeaders(table)
        params = []
        param = {}
        tableBody = table.tbody
        rows = tableBody.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            for i in range(0, len(cols)):
                param[headers[i]] = cols[i].text
            # append params
            params.append(param)
            param = {}
        return params

    def __getCommandExample(self, article):
        pass

    def __getResponseExample(self, article):
        pass

    def __getTableHeaders(self, table):
        '''
        Extract the headers of the description table

        Returns:
        --------
        List: headers
        '''
        tableHead = table.thead
        row = tableHead.tr
        cols = row.find_all('th')
        headers = []
        # get text only
        for col in cols:
            headers.append(col.text)
        return headers

    def __dumpCommandToFile(self, commandName, data):
        '''
        Creates a json file for the command: commandName

        Returns:
        --------
        True | Raise exception
        '''
        try:
            p = os.path.join(self.absolute_dirpath,
                             '../commands/' + commandName + '.json')
            f = open(p, "w")
            json.dump(data, f)
            f.close()
            print('Command file created: ', p)
            return True
        except Exception:
            raise Exception("Couldn't create a file for the command: " +
                            commandName)

    def __getCommandData(self, article, table):
        '''
        Gather all command data in a list and return it

        Returns:
        --------
        Dictionary: data
        '''
        try:
            data = {}
            data['command'] = self.__getCommandName(article)
            data['description'] = self.__getCommandDescription(article)
            data['availability'] = self.__getCommandAvailability(article)
            data['paramaters'] = self.__getCommandParameters(table)
            return data
        except Exception as e:
            raise e

    # scrap commands
    def scrapCommands(self):
        '''
        Executes the scrap process

        Returns:
        --------
        Null
        '''

        # get all commands urls, ending with .md
        urls = self.__getURLs([self.gitHubURL])

        for url in urls:
            try:
                article, table = self.__getParsedPage(url)
                commandName = self.__getCommandName(article)
                data = self.__getCommandData(article, table)
                self.__dumpCommandToFile(commandName, data)
            except Exception as e:
                print(
                    "Couldn't extract command because documentation differs in URL: "
                    + url + " \nReason: " + str(e))

        print('\nCommands count: ' + str(len(urls)))
        print('Command finished.')
