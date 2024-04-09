# Debt Wally BOT

Bot de Telegram para gestionar las cuentas de casa como forma de repartir los gastos.

## TODO

- [ ] Auto calcular lo que hay que pagar de alquier
- [ ] Configurar cuanto es el aquiler
- [ ] Recordatorio de pago (puede que no se pueda puesto que se pone en stand-by)
- [ ] Funcionalidad de lista de la compra
- [ ] Lista de commandos

## Run on docker

``` bash
docker run -p 5000:5000 -e BOT_TOKEN=<your_bot_token> -e URL=<your_webhook_url> my-telegram-bot
```