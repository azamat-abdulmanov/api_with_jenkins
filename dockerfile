FROM python
WORKDIR /usr/workspace
COPY requirements.txt .
COPY test_api.py .
RUN mkdir allure-results
RUN pip install -r requirements.txt
CMD ["pytest", "test_api.py", "--alluredir=allure-results"]

