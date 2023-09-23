This is a simple web spider CLI app for Parthenon Software Group.

To run the app, simply navigate to the root directory, run pipenv install to install the dependencies and then run python spider.py to start the app.

The app will request the following inputs:

- Target URL - this is the URL where the spider will start crawling

- Max Recursion Depth - this is the maximum number of links the spider will follow before stopping

- Spider Asserts? - this is a boolean value that determines whether the spider will capture should capture page assets such as images, css, and     javascript files. If set to false the spider will only capture links contained in <a href> tags.

- Use rate limiting? - this is a boolean value that determines whether the spider will limit the number of requests it makes per second. If set to true, you will be prompted to enter the number of requests per second you would like to limit the spider to.

- Enter max threads - this is the maximum number of threads the spider will use to make requests. If set to 1, the spider will run in a single thread. Higher numbers will generally result in faster execution, but may cause issues with some sites.

- Start Spider? - enter y to start the spider, or if you wish to go back and change any of the previous inputs, enter n and the app will restart.


Notes:

This is a CLI based app so it is best to run it in a seperate terminal window. Running it in an IDE such as PyCharm or VS Code will work, but the output may not be formatted correctly.

-------------------------

Captured file will be saved in the root directory of the app. The folder names will be based on the URL where the file was found.
A UTC time stamp will be appended to the folder name to preserve the time at which the file was captured.

-------------------------

Rate limiting and Max threads should be adjusted to avoid overloading the target server. If the spider is making too many requests per second, or using too many threads, the target server may block the spider's IP address. If this happens, the spider will stop and you will need to restart the app. A good starting point is around 5 requests per second for rate limiting and max threads also set to 5.
If you're seeing a lot of errors in the output, try using a lower value for rate limiting and max threads. 

-------------------------

Some website do not allow web crawlers to access their site. If you are having trouble crawling a site, try using a different target URL. For example, https://www.google.com will not work, but https://www.google.com/search?q=parthenon will work.

