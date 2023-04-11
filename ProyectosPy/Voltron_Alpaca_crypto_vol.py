# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 17:55:43 2023

@author: Miguel_Perez_Diaz
"""
import requests
import pandas as pd
import config
import time
import sys
import datetime
import logging


# funcion para calcular RSI
# Version manual,usar Pandas_TA para indicadores automaticos
# Respetar nombre de funcion,parametros y orden de los mismos
# para no tener que cambiar todo
def RSI(df, periodos=14, ema=True):
    print("==== Funcion RSI() ====")
    if len(df.index) < periodos:
        print("No hay suficientes datos para calculo RSI - Funcion RSI()")
        sys.exit("Insuficiente Market Data para calcular RSI")
        logging.error(
            ' ====ERROR!!! Insuficiente Market Data para calcular RSI ===='
        )
        return -1
    else:

        # RSI tiene 2 formulas

        # ====FORMULA RSI PASO 1 Fuerza Relativa de 14 ruedas=======
        # diff() calcula la diferencia entre el valor de esta fila
        # y el de la fila anterior,para toda la serie de datos
        diferencia_cierre = df['Close'].diff()

        # cierres positivos y negativos normalizados
        # clip() evita que los valores de una serie superen o
        # esten debajo de un valor especifico
        # la seria tiene valores negativos,se fuerzan a 0
        # solo se aceptan valores positivos en cada serie
        cierres_positivos = diferencia_cierre.clip(lower=0)
        cierres_negativos = -1 * diferencia_cierre.clip(upper=0)

        # usar media exponencial
        # para suavizar los resultados
        cierres_positivos_suave = cierres_positivos.ewm(com=periodos - 1,
                                                        adjust=True,
                                                        min_periods=periodos
                                                        ).mean()

        cierres_negativos_suave = cierres_negativos.ewm(com=periodos - 1,
                                                        adjust=True,
                                                        min_periods=periodos
                                                        ).mean()

        rsi = cierres_positivos_suave / cierres_negativos_suave

        # ====FORMULA RSI PASO 2 Obtener Indice de Fuerza Relativa =======
        rsi = 100 - (100/(1 + rsi))

        print("RSI actual: ", rsi, " - Funcion RSI()")
        return rsi

# generar una senal de trading a partir de un dataframe
# que contenga ya calculado el metodo a utilizar


def senal_trading(datos, metodo="RSI"):
    print("==== Funcion senal_trading() ====")
    if metodo == "RSI":
        # RSI es una serie,solo necesitamos el dato mas reciente
        if datos['RSI'].tail(1).values <= RSI_BUY_ZONE:
            print(ticker,
                  " con RSI <= a ",
                  RSI_BUY_ZONE,
                  datos['RSI'].tail(1).values, " Funcion senal_trading()")

            # estoy en zona de compra por sistema
            # pero ya estoy comprado de antes
            # enviar senal HOLD
            if comprado == True:
                print("==Ya tenemos posicion HOLDING - Funcion senal_trading()==")
                logging.warning(' RSI: ' +
                                str(datos['RSI'].tail(1).values) +
                                " comprado HOLD!")
                return "HOLD"

            else:
                # no estoy comprado y hay senal,enviar senal de compra
                # la compra no sucede aqui,solo se detecta senal
                logging.warning(
                    ' RSI: ' +
                    str(datos['RSI'].tail(1).values) +
                    " sin posicion, BUY!")
                return "BUY"

        # estoy en zona de venta por sistema
        if datos['RSI'].tail(1).values >= RSI_SELL_ZONE:
            print(ticker,
                  " con RSI >= a ",
                  RSI_SELL_ZONE,
                  datos['RSI'].tail(1).values, " Funcion senal_trading()")

            if comprado == True:
                print("==SELLING - Funcion senal_trading()==")
                return "SELL"
            else:
                print("==CANT SHORT CRYPTO IN ALPACA WAIT - Funcion senal_trading()=")
                logging.warning(
                    ' RSI: ' +
                    str(datos['RSI'].tail(1).values) +
                    " CANT SHORT CRYPTO IN ALPACA WAIT - Funcion senal_trading()")

                return "WAIT"

        else:
            # no estoy en zona de compra ni de venta,esperar
            print(ticker, " sin senal aun,RSI=", datos['RSI'].tail(
                1).values, " - Funcion senal_trading()")
            return "WAIT"


def puedo_operar():

    print("==== Funcion puedo_operar()")
    # Trading API (cada una es distinta)
    api_url_market = "https://paper-api.alpaca.markets/v2"

    # Endpoint Cuenta Comitente
    api_market_comitente = "/account"

    headers = {
        'accept': 'application/json',
        "APCA-API-KEY-ID": config.api_key_id,
        "APCA-API-SECRET-KEY": config.api_secret_id

    }

    status_OK = 200

    ask = market_data_quote_crypto()
    # suficiente cash para operar la postura al precio actual
    # con el minimo de contratos que deseo
    cash_minimo_necesario = float(ask)*postura*minimo_contratos_operables

    response = requests.get(api_url_market+api_market_comitente,
                            headers=headers
                            )

    if response.status_code == status_OK:
        # pedimos los datos en formato JSON
        print("Conexion Broker OK - Funcion puedo_operar()")

        api_response = response.json()

        api_response_df = pd.json_normalize(api_response)

        if (
                api_response_df['status'].values == "ACTIVE"
            ) and \
                   \
            (
                api_response_df['crypto_status'].values == "ACTIVE"
        ) and \
                   \
            (
            float(
                api_response_df['buying_power'].values) > cash_minimo_necesario
        ) and \
                   \
            (
            float(api_response_df['cash'].values) > cash_minimo_necesario
        ):

            print("Comitente Activa - Funcion puedo_operar()")
            print("Buying Power OK.Cash OK- Funcion puedo_operar()")
            print("Trading OK- Funcion puedo_operar()")
            #logging.info(str(datetime.datetime.today())+' Comitente Activa')
            return True

        else:

            print("Error en cuenta comitente,chequear Broker")
            print(
                "Status:", api_response_df['status'])
            print("Crypto Status:",
                  api_response_df['crypto_status'])
            print("BuyingPower:",
                  api_response_df['buying_power'])
            print("Cash:", api_response_df['cash'])
            print("Minimo cash para operar: ",
                  cash_minimo_necesario)

            logging.error(
                '===== ERROR CUENTA COMITENTE =====')
            logging.error("Status: "+api_response_df['status'])
            logging.error("BuyingPower: "+api_response_df['buying_power'])
            logging.error("Minimo cash para operar: "+cash_minimo_necesario)
            logging.shutdown()
            sys.exit("Cuenta no habilitada para Trading - Abort")

    else:
        print("Error! ", response.status_code)
        logging.error(
            'No hay conexion con Broker - Abort' +
            " Status Code: " +
            str(response.status_code))
        logging.shutdown()
        sys.exit("No hay conexion con Broker - Abort")
        return False

# Actual Buy


def enviar_orden(ticker, contratos, buy_sell="buy", order_type="market",
                 order_time_force="gtc", order_class="simple"):

    # Esta funcion recibe la variable "postura" como parametro "contratos"
    # toda vez que es llamda por la funcion estrategia_RSI().
    # Cuando es llamada por manejo_posicion() recibe "qty" como parametro
    # "contratos".
    print("==== Funcion enviar_orden() ====")

    global comprado, posicion_actual, contratos_enmano, RSI_STOPLOSS, RSI_Actual
    # Trading API (cada una es distinta)
    api_url_market = "https://paper-api.alpaca.markets/v2"

    api_orders = "/orders"

    headers = {
        'accept': 'application/json',
        "APCA-API-KEY-ID": config.api_key_id,
        "APCA-API-SECRET-KEY": config.api_secret_id

    }

    status_OK = 200

    # mi posicion
    # contratos=0.01
    # buy_sell="buy"
    # order_type="market"
    # order_time_force="gtc"
    # order_class="simple"

    params = {
        "symbol": ticker,
        "qty": contratos,
        "side": buy_sell,
        "type": order_type,
        "time_in_force": order_time_force,
        "order_class": order_class

    }

    status_OK = 200

    # get vs post
    # prestar especial atencion a la linea
    # json=params
    # normalmente ahi ponemos params=params
    # porque son los parametros de la funcion
    # en este caso la API pide que la orden en si
    # este en formato JSON
    # poniendo json=params tranformamos el diccionario de arriba
    # en formato json
    response = requests.post(api_url_market+api_orders,
                             json=params,
                             headers=headers,
                             timeout=5
                             )
    api_response = response.json()
    api_response_df = pd.json_normalize(api_response)
    print(api_response_df['status'].values)

    if response.status_code == status_OK:
        # pedimos los datos en formato JSON
        print("Conexion OK - Funcion enviar_orden()")
        api_response = response.json()
        #print("Respuesta del server ",api_response)

        api_response_df = pd.json_normalize(api_response)

        if (api_response_df['status'].values == "accepted" or
                api_response_df['status'].values == "pending_new"):
            print("Orden aceptada por el Mercado - Funcion enviar_orden()")
            print("Orden ID:",
                  api_response_df['id'].values, " - Funcion enviar_orden()")
            print(
                "Orden Time:", api_response_df['submitted_at'].values,
                " - Funcion enviar_orden()")
            print("Orden Status:",
                  api_response_df['status'].values, " - Funcion enviar_orden()")
            print("Orden Fill Status:",
                  api_response_df['filled_at'].values, " - Funcion enviar_orden()")

            if buy_sell == "buy":
                comprado = True
                # RSI_STOPLOSS=RSI_Actual-10
                logging.warning(
                    " ==== BOUGHT! ====")

                logging.warning(
                    ticker +
                    "@" +
                    str(api_response_df['filled_avg_price'].values) +
                    "AVG")

                logging.warning(
                    ticker +
                    " Order Requested QTY " +
                    str(api_response_df['qty'].values) +
                    "/ Order FILLED QTY " +
                    str(api_response_df['filled_qty'].values))

                # update portfolio
                posicion_actual['comprado'] = True
                posicion_actual['symbol'] = api_response_df['symbol'].values
                posicion_actual['contratos'] = api_response_df['qty'].values
                posicion_actual['avgprice'] = api_response_df['filled_avg_price'].values
                posicion_actual['direccion'] = api_response_df['side'].values
                posicion_actual['filled'] = api_response_df['filled_at'].values
                posicion_actual['filledqty'] = api_response_df['filled_qty'].values

                contratos_enmano = postura

            if buy_sell == "sell":

                # me queda posicion todavia o no?
                if (contratos_enmano-contratos > 0):
                    comprado = True
                    contratos_enmano = round(
                        (contratos_enmano-contratos), 2
                    )
                else:
                    comprado = False

                    # update portfolio
                    posicion_actual['comprado'] = None
                    posicion_actual['symbol'] = None
                    posicion_actual['contratos'] = None
                    posicion_actual['avgprice'] = None
                    posicion_actual['direccion'] = None
                    posicion_actual['filled'] = None
                    posicion_actual['filledqty'] = None

                logging.warning(
                    " ==== SOLD! ====")

                logging.warning(
                    " Orden ID:" +
                    str(api_response_df['id'].values) +
                    " Orden Fill Status:" +
                    str(api_response_df['filled_at'].values))

        else:
            logging.error(
                " Orden Rechazada!!! Linea 378 - Funcion enviar_orden()")

            sys.exit(
                "La orden fue rechazada!! - Linea 381 - Funcion enviar_orden()")

        return api_response_df
    else:
        print("Error! ", response.status_code)
        logging.error(" Orden Rechazada!!! " +
                      "Status Code: " +
                      str(response.status_code))
        logging.shutdown()
        sys.exit("La orden no pudo enviarse!")

    return


def estrategia_RSI(precios):

    print("====  Funcion estrategia_RSI() ====")
    # traer suficientes precios para calcular RSI
    precios_historicos_activo = precios

    # calcular  RSI
    precios_historicos_activo['RSI'] = RSI(precios_historicos_activo)

    # Hay compra basandonos en RSI?
    Senal = senal_trading(precios_historicos_activo, "RSI")

    if (Senal == "BUY" and comprado == False):
        compra = enviar_orden(ticker,
                              postura,
                              buy_sell="buy",
                              order_type="market",
                              order_time_force="gtc",
                              order_class="simple")

        print("==========Compra!====== Funcion estrategia_RSI()")
        logging.warning(
            " ==== Senal Compra RSI ====="
        )

        return precios_historicos_activo['RSI'].tail(1).values

    if (Senal == "SELL" and comprado == True):
        venta = enviar_orden(ticker,
                             postura,
                             buy_sell="sell",
                             order_type="market",
                             order_time_force="gtc",
                             order_class="simple")

        print("==========Venta!====== Funcion estrategia_RSI()")
        logging.warning(

            " ==== Senal Venta RSI ===="
        )

        return precios_historicos_activo['RSI'].tail(1).values

    if Senal == "HOLD" or Senal == "WAIT":
        logging.info(" HOLD or WAIT RSI")
        return precios_historicos_activo['RSI'].tail(1).values
    else:
        return precios_historicos_activo['RSI'].tail(1).values


def market_data_quote_crypto(symbol="BTC/USD"):

    print("==== Funcion market_data_quote_crypto() ====")

    # dont be that asshole
    time.sleep(2)

    headers = {
        'accept': 'application/json',
        "APCA-API-KEY-ID": config.api_key_id,
        "APCA-API-SECRET-KEY": config.api_secret_id

    }

    # just Coinbase
    params = {
        "symbols": symbol,

    }

    # Endpoints
    # api_url_data_crypto = "https://data.alpaca.markets/v1beta1/crypto"
    #api_marketdata_latest = "/"+ticker+"/quotes/latest"
    api_url_data_crypto = "https://data.alpaca.markets/v1beta3/crypto/us"
    api_marketdata_latest = "/latest/quotes"

    response = requests.get(api_url_data_crypto+api_marketdata_latest,
                            params=params,
                            headers=headers,
                            timeout=5
                            )

    # Nos pudimos conectar correctamente
    # Nunca deberiamos avanzar si hay un error aqui
    if response.status_code == status_OK:
        # pedimos los datos en formato JSON
        #print("Conexion OK ")

        # Un Response contiene ademas del OK 200, una porcion de datos
        # esos datos estan en formato JSON
        # con esto obtenermos solo los datos del Response,en ese formato
        api_response = response.json()

        # get ask
        print("Respuesta completa -> ", api_response['quotes'][str(symbol)], ":\n",
              "Timestamp -> ", api_response['quotes'][str(symbol)]['t'], "\n",
              "Ask Price -> ", api_response['quotes'][str(symbol)]['ap'],
              " - Funcion market_data_quote_crypto()")

        logging.info(
            ticker+"@" +
            str(api_response['quotes'][str(symbol)]['ap'])
        )

        return api_response['quotes'][str(symbol)]['ap']

    else:
        print("Error! ", response.status_code,
              " - Funcion market_data_quote_crypto()")
        logging.error(" ERROR obteniendo quotes!!!" +
                      " Status Code: " +
                      str(response.status_code))
        sys.exit("Error en Conexion! Linea: 476")


def market_data(ticker, desde, hasta, intervalo):

    print("==== Funcion market_data() ==== ")
    #datos=yf.download(ticker, start=desde, end=hasta,interval=intervalo)

    # formtear el input en datetime standard a ISO RFC-3339
    # tal cual pide la documentacion
    # cada API es distinta
    # si,hay varias maneras de hacer esto,esta es la mas directa
    # datetime standard Python 2022-01-08 02:36:03.198203
    # datetieme ISO RFC-3339 2022-02-06T0:00:00Z
    desde = desde.isoformat()[:-7] + 'Z'
    hasta = hasta.isoformat()[:-7] + 'Z'

    # Market Data API (cada una es distinta)
    #api_url_data = "https://data.alpaca.markets/v1beta1/crypto"
    api_url_data = "https://data.alpaca.markets/v1beta3/crypto/us"
    #GET /{symbol}/bars

    # Endpoint OHLC
    api_marketdata_OHLC = "/bars"

    headers = {
        'accept': 'application/json',
        "APCA-API-KEY-ID": config.api_key_id,
        "APCA-API-SECRET-KEY": config.api_secret_id

    }

    # la documentacion indica que parametros
    # son opcionales y cuales no
    params = {
        "symbols": ticker,  # requiired
        # "exchanges": "CBSE",
        "start": desde,  # optional
        "timeframe": intervalo  # required
    }

    # El codigo de response 200 establece que la conexion fue OK
    # no quiere decir que los datos que recibamos sean los correctos
    # solamente que nos pudimos conectar sin problemas.
    status_OK = 200
    status_faltanparametros = 422
    status_demasiados_requests = 429
    status_sin_autorizacion = 403
    status_parametro_invalido = 400

    response = requests.get(api_url_data+api_marketdata_OHLC,
                            params=params,
                            headers=headers,
                            timeout=5
                            )

    if response.status_code == status_OK:
        # pedimos los datos en formato JSON
        print("MarketData-Conexion OK - Funcion market_data()")

        api_response = response.json()
        #print("Respuesta del server ",api_response)

        api_response_df = pd.json_normalize(api_response['bars'])

        # ==== Comienzo de modificación del response ====
        i = 0
        ohlc = list(api_response_df["BTC/USD"])
        ohlc2 = []
        while i <= len(ohlc[0])-1:
            ohlc2.append(ohlc[0][i])
            i = i + 1
        # ===== Fin de modificacion ====
        api_response_df2 = pd.DataFrame(ohlc2)

        # Formateo
        # Queremos las fechas como index
        api_response_df2.set_index("t", inplace=True)

        # Queremos que los nombres de las columnas sean los de YFinance
        api_response_df2.rename(

            columns={
                "o": "Open",
                "h": "High",
                "l": "Low",
                "c": "Close",
                "v": "Volume",

            },

            inplace="True"

        )

        api_response_df2.index.rename("Date", inplace=True)
        logging.info(
            ' == Market Data Actualizada ==')

    else:
        print(" Error! ", response.status_code)
        logging.error(' ==ERROR de Market Data==' +
                      "Status Code: " +
                      str(response.status_code), " - Funcion market_data()")
        logging.shutdown()

        sys.exit("Sin conexion a Market Data-Abort")
        return

    return api_response_df2


def liquidate_posicion(ticker):

    print("==== Funcion liquidate_posicion()====")
    global comprado, posicion_actual, contratos_enmano
    # Trading API (cada una es distinta)
    api_url_market = "https://paper-api.alpaca.markets/v2"

    api_orders = "/positions/"+ticker

    headers = {
        'accept': 'application/json',
        "APCA-API-KEY-ID": config.api_key_id,
        "APCA-API-SECRET-KEY": config.api_secret_id

    }

    status_OK = 200

    # explicar DELETE!!!
    response = requests.delete(api_url_market+api_orders,
                               headers=headers
                               )

    if response.status_code == status_OK:
        # pedimos los datos en formato JSON
        print("Conexion OK ")
        api_response = response.json()
        #print("Respuesta del server ",api_response)

        api_response_df = pd.json_normalize(api_response)
        if (api_response_df['status'].values == "accepted"):
            print("Orden aceptada por el Mercado - Funcion liquidate_posicion()")
            print(
                "Orden ID:", api_response_df['id'].values, " - Funcion liquidate_posicion()")
            print(
                "Orden Time:", api_response_df['submitted_at'].values, " - Funcion liquidate_posicion()")
            print("Orden Status:",
                  api_response_df['status'].values, " - Funcion liquidate_posicion()")
            print("Orden Fill Status:",
                  api_response_df['filled_at'].values, "- Funcion liquidate_posicion()")

            comprado = False
            contratos_enmano = 0

            # update portfolio
            posicion_actual['comprado'] = None
            posicion_actual['symbol'] = None
            posicion_actual['contratos'] = None
            posicion_actual['avgprice'] = None
            posicion_actual['direccion'] = None
            posicion_actual['filled'] = None
            posicion_actual['filledqty'] = None

            logging.warning(
                " !!!==== LIQUIDATION! ====!!!")

            logging.warning(
                " Orden ID:" +
                str(api_response_df['id'].values) +
                " Orden Fill Status:" +
                str(api_response_df['filled_at'].values))

        else:
            logging.error(
                "===== Orden Rechazada!!! ")
            logging.shutdown()
            sys.exit("La orden fue rechazada!!")

        return api_response_df
    else:
        print("Error! ", response.status_code)
        logging.error(

            " Orden Rechazada!!! " +
            "Status Code: " +
            str(response.status_code), "- Funcion liquidate_posicion()"
        )

        # error cuando todavia hay posicion abierta!!!
        if contratos_enmano > 0:
            logging.error(

                " ========CERRAR A MANO POSICIONES ABIERTAS!!! ==== ")

        logging.shutdown()
        sys.exit("La orden no pudo enviarse!")

        return

    return


def manejo_posicion(comprado, contratos_enmano, posicion_actual, RSI_Actual):

    print("==== Funcion manejo_posicion()====")
    global postura, RSI_STOPLOSS, RSI_BUY_ZONE

    # debug
    logging.info('== UPDATE POSICION ==')

    logging.info('== CONTRATOS EN MANO ' +
                 str(contratos_enmano) +
                 " ==")

    logging.info('== Comprado? ' +
                 str(comprado) +
                 " ==")

    logging.info('== RSI_ACTUAL ' +
                 str(RSI_Actual) +
                 " ==")

    logging.info('== RSI_STOPLOSS ' +
                 str(RSI_STOPLOSS) +
                 " ==")

    logging.info('== RSI_TARGET1 ' +
                 str(RSI_TARGET1) +
                 " ==")

    logging.info('== RSI_TARGET2 ' +
                 str(RSI_TARGET2) +
                 " ==")

    logging.info('== RSI_TARGET3 ' +
                 str(RSI_TARGET3) +
                 " ==")

    if comprado == True:
        # vender de acuerdo a targets RSI

        # vendemos un tercio de la posicion en cada target
        if (RSI_Actual >= RSI_TARGET1) and (contratos_enmano == postura):

            qty = round((postura/3), 2)

            logging.warning(str(datetime.datetime.today()) +
                            '== Target 1 ACTIVADO!!! ==')
            logging.warning(str(datetime.datetime.today()) +
                            '== Vendiendo una parte==')
            enviar_orden(ticker, qty, "sell")

            # mover stop loss
            RSI_STOPLOSS = RSI_TARGET1-20
            return

        # explicar decimales
        if (RSI_Actual >= RSI_TARGET2) and (
                contratos_enmano ==
                round(
                    (
                        (postura/3)*2
                    ),
                    2)
        ):

            qty = round((postura/3), 2)

            logging.warning(
                '== Target 2 ACTIVADO!!! ==')
            logging.warning(
                '== Vendiendo una parte==')
            enviar_orden(ticker, qty, "sell")

            # mover stop loss
            RSI_STOPLOSS = RSI_TARGET2-15
            return

        if (RSI_Actual >= RSI_TARGET3) and (
                contratos_enmano ==
                round(
                    (
                        (postura/3)
                    ),
                    2)
        ):
            qty = round((postura/3), 2)

            logging.warning(
                '== Target 3 ACTIVADO!!! ==')
            logging.warning(
                '== Vendiendo una parte==')
            enviar_orden(ticker, qty, "sell")

            # sin posicion reset stop loss
            RSI_STOPLOSS = RSI_BUY_ZONE-20
            logging.info('== NUEVO STOP LOSS ' +
                         str(RSI_STOPLOSS) +
                         " ==")
            return

        # stop loss
        if (RSI_Actual <= RSI_STOPLOSS) and (contratos_enmano > 0):

            # liquidar todas las posiciones por las dudas y salir
            liquidate_posicion(ticker)

            logging.warning(
                '== STOP LOSS ACTIVADO!!! ==')
            logging.warning(
                '== Liquidando posiciones==')
            comprado = "False"
            RSI_STOPLOSS = RSI_BUY_ZONE-20
            logging.info('== STOP LOSS ' +
                         str(RSI_STOPLOSS) +
                         " ==")
            return

        logging.info('== COMPRADO CONTRATOS ' +
                     str(contratos_enmano) +
                     " ==")
        logging.info('== STOP LOSS ' +
                     str(RSI_STOPLOSS) +
                     " ==")

    else:
        # sin posicion ,nada para hacer
        logging.info('== STOP LOSS ' +
                     str(RSI_STOPLOSS) +
                     " ==")
        return

# Operatoria


def bot():
    print("------------ Funcion bot() ----------")

    # cuenta habilitada?
    comitente = puedo_operar()

    if comitente == True:
        ask = market_data_quote_crypto()

        RSI_Actual = float(estrategia_RSI(market_data_hist))
        manejo_posicion(comprado, contratos_enmano,
                        posicion_actual, RSI_Actual)

    else:
        print("Error - Funcion bot()")
        logging.shutdown()
        sys.exit("Error!!!")


# ==================COMIENZO PROGRAMA PRINCIPAL================

print("==== Comienzo Programa principal ====", "/n")
print("/n")
print("===SETUP OPCIONES=== ")

# ===SETUP OPCIONES===

# logging config
# append to file
LOG_FORMAT = '%(name)s | %(funcName)s | %(lineno)d | %(levelname)s | %(asctime)s | %(message)s'

logging.basicConfig(level=logging.INFO,
                    filename=str(
                        datetime.datetime.today().strftime(
                            "%d-%m-%Y-%H_%M_%S")
                    )+' pepino_bot.log',
                    filemode='a',
                    format=LOG_FORMAT)

hoy = datetime.datetime.today()

# ticket
ticker = "BTC/USD"

# cada API es distinta,leer siempre la documentacion
# https://alpaca.markets/docs/api-documentation/api-v2/account/
api_url = "https://paper-api.alpaca.markets/v2"


# suficiente para calcular RSI y MACD
marketdata_limit = 200

# El codigo de response 200 establece que la conexion fue OK
# no quiere decir que los datos que recibamos sean los correctos
# solamente que nos pudimos conectar sin problemas.
status_OK = 200

# position sizing multiples targets
postura = 0.03

# que haya cash para operar n contratos minimo
# crypto en Alpaca opera sobre cash, no margin en papertrading al menos
# en general le voy a pedir 3 veces la postura
minimo_contratos_operables = 3

# comprado?
# deberiamos consultarlo (confirmarlo) ni bien arranque el bot
comprado = False

contratos_enmano = 0

# RSI config
# cambiar para tener mas/menos senales
RSI_SELL_ZONE = 65
RSI_BUY_ZONE = 35

# Manejo de posicion usando RSI
RSI_TARGET1 = 55
RSI_TARGET2 = 60
RSI_TARGET3 = 65

RSI_STOPLOSS = RSI_BUY_ZONE-10


posicion_actual = {
    "comprado": None,
    "symbol": None,
    "contratos": None,
    "avgprice": None,
    "direccion": None,
    "filled": None,
    "filledqty": None
}


# =======================================
logging.info(' ======BOT START======')
print("====BOT START==== Programa Principal", "/n")
print("/n")
# dont be that asshole
start_market_data_clock = time.time()
print("Primera consulta a market_data()", "/n")
market_data_hist = market_data(ticker, hoy, hoy, "1Min")


while True:
    print("==== WHILE ====", "/n", "llamo al bot()")

    bot()

    print("==== ya volvi del bot()====")

    if (time.time() - start_market_data_clock) > 60:
        print("====Paso 1 Minuto-Refrescando Market Data==== - WHILE ")
        logging.info(
            ' Paso 1 Minuto-Refrescando Market Data')
        market_data_hist = market_data(ticker, hoy, hoy, "1Min")

        # resetear reloj
        start_market_data_clock = time.time()
