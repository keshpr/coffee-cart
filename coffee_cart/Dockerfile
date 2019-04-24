FROM python:3
ENV PYTHONUNBUFFERED 1

RUN pip3 install django-cors-headers

RUN mkdir -p /app/coffee_cart
WORKDIR /app/coffee_cart
COPY requirements.txt /app/coffee_cart/
RUN pip install -r requirements.txt
COPY . /app/coffee_cart/

RUN chmod +x /app/coffee_cart/entrypoint.sh

ENTRYPOINT [ "/app/coffee_cart/entrypoint.sh" ]