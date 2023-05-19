import streamlit as st
from time import sleep
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

# Enunciado
linha = '-=-=' * 12
st.markdown("<h1 style='text-align: center;'>SIMULADOR DE INVESTIMENTO EM RENDA FIXA</h1>", unsafe_allow_html=True)

# Informações importantes
st.markdown('''
    <div style='text-align: center;'>
        <p style='color: green; margin: 0;'>* Valor da SELIC atual: 13.75% *</p>
        <p style='color: green; margin: 0;'>* Valor do CDI atual: 13.65% *</p>
    </div>
    ''', unsafe_allow_html=True)

# Informações importantes
#st.markdown("<p style='text-align: center; color: green;'>Valor do CDI atual: <span style='color: yellow;'>13.65%</span></p>", unsafe_allow_html=True)
#st.write(linha)

# Inputs
valor = st.number_input('Qual o valor do investimento: R$ ')
tempo = st.number_input('Por quanto tempo o capital ficará investido? ')
unidade = st.selectbox('O período acima, representa, Mes(es) ou Ano(s)?', ['Mes(es)', 'Ano(s)']).lower()
index = st.selectbox('Qual o indexador para este investimento?', ['CDI', 'PREFIXADO', 'SELIC', ]).lower()
taxa = st.number_input('Qual a porcentagem de ganho do indexador? ')
vlr_imposto = st.number_input('Qual o valor cobrado de imposto (I.R) na liquidez deste título? ')

if st.button('Calcular'):
    if unidade == 'Meses':
        tempo = float(tempo) / 12
    else:
        tempo = float(tempo)

    today = date.today() + relativedelta(years=tempo)
    data_liquidez = today.strftime("%d/%m/%Y")

    st.write('Obrigado pelas informações, por favor, aguarde um instante enquanto organizo os dados...')
    sleep(6)
    st.write('Pronto...')
    sleep(2)
    st.write('--> O valor investido será de <font color="blue">R$ {:.2f}</font>.'.format(valor),unsafe_allow_html=True)
    if unidade != 'meses':
        tempo_ano = tempo
        st.write('--> O tempo será de <font color="blue">{}</font> ano(s).'.format(tempo_ano),unsafe_allow_html=True)
    else:
        tempo_meses = tempo * 12
        st.write(('--> O tempo será de <font color="blue">{}</font> mes(es).'.format(tempo_meses)),unsafe_allow_html=True)

    st.write('-->   O indexador escolhido foi <font color="blue">{}</font>.'.format(index.upper()), unsafe_allow_html=True)
    st.write('-->   O rendimento será de <font color="blue">{}%</font> sob <font color="blue">{}</font>.'.format(taxa, index.upper()),unsafe_allow_html=True)
    st.write('-->   O taxa descontada pelo I.R será de <font color="blue">{}%</font>'.format(vlr_imposto),unsafe_allow_html=True)
    st.write('-->   A data de liquidez p/ este investimento será dia <font color="blue">{}</font>'.format(data_liquidez),unsafe_allow_html=True)

    st.write('Agora, irei calcular os resultados finais aproximados do seu investimento, aguarde enquanto faço as contas por aqui...')
    sleep(10)
    st.write('Pronto, confira abaixo o resultado aproximado deste investimento...')
    sleep(5)

    # Variáveis
    tx_selic = 13.75
    tx_cdi = tx_selic - 0.10
    anual = (valor/100)*tx_selic + valor
    mensal_cdi = ((taxa/100)*tx_cdi)/12
    mensal_selic = ((taxa/100)*tx_selic)/12
    mensal_prefixado = ((taxa / 100) * taxa) / 12
    anual_cdi = (taxa/100)*tx_cdi
    anual_selic = (taxa/100)*tx_selic
    anual_prefixado = taxa

    # Variáveis de Juros Compostos
    # M = C.(1+i)^t
    liquidez_selic = valor * (1 + anual_selic / 100) ** tempo
    liquidez_cdi = valor * (1 + anual_cdi / 100) ** tempo
    liquidez_prefixado = valor * (1 + anual_prefixado / 100) ** tempo
    desc_imposto_selic = (liquidez_selic - valor) * (vlr_imposto / 100)
    desc_imposto_cdi = (liquidez_cdi - valor) * (vlr_imposto / 100)
    desc_imposto_prefixado = (liquidez_prefixado - valor) * (vlr_imposto / 100)
    liquidez_real_selic = liquidez_selic - desc_imposto_selic
    liquidez_real_cdi = liquidez_cdi - desc_imposto_cdi
    liquidez_real_prefixado = liquidez_prefixado - desc_imposto_prefixado

    if index == 'selic':
        st.write('--> O rendimento mensal é aproximadamente de <font color="green">{:.3f}%'.format(mensal_selic),unsafe_allow_html=True)
        st.write('--> O rendimento anual é aproximadamente de <font color="green">{:.3f}%'.format(anual_selic),unsafe_allow_html=True)
        st.write('--> O valor informado do I.R foi de <font color="green">{}%</font>, equivalente a <font color="green">R$ {:.2f}</font> do montante final.'.format(vlr_imposto, desc_imposto_selic),unsafe_allow_html=True)
        st.write('--> O valor na liquidez já descontado o I.R será de aproximadamente <font color="green">R$ {:.2f}'.format(liquidez_real_selic),unsafe_allow_html=True)
    elif index == 'cdi':
        st.write('--> O rendimento mensal é aproximadamente de <font color="green">{:.3f}%</font>'.format(mensal_cdi),unsafe_allow_html=True)
        st.write('--> O rendimento anual é aproximadamente de <font color="green">{:.3f}%</font>.'.format(anual_cdi),unsafe_allow_html=True)
        st.write('--> O valor informado do imposto foi de <font color="green">{}%</font>, equivalente a <font color="green">R$ {:.2f}</font> do montante final.'.format(vlr_imposto, desc_imposto_cdi),unsafe_allow_html=True)
        st.write('--> O valor na liquidez já descontado o I.R será de aproximadamente <font color="green">R$ {:.2f}</font>'.format(liquidez_real_cdi),unsafe_allow_html=True)
    else:
        st.write('--> O rendimento mensal é aproximadamente de <font color="green">{:.3f}%</font>'.format(mensal_prefixado),unsafe_allow_html=True)
        st.write('--> O rendimento anual é aproximadamente de <font color="green">{:.3f}%</font>.'.format(anual_prefixado), unsafe_allow_html=True)
        st.write('--> O valor informado do imposto foi de <font color="green">{}%</font>, equivalente a <font color="green">R$ {:.2f}</font> do montante final.'.format(vlr_imposto, desc_imposto_prefixado), unsafe_allow_html=True)
        st.write('--> O valor na liquidez já descontado o I.R será de aproximadamente <font color="green">R$ {:.2f}</font>'.format(liquidez_real_prefixado), unsafe_allow_html=True)

    data_atual = date.today()
    data_formatada = data_atual.strftime("%d/%m/%Y")
    st.write("Simulação realizada em", data_formatada,)
    st.write('<font color="yellow">Muito obrigado por usar nosso simulador, espero ter te ajudado. Desejamos ótimos investimentos!!!</font>', unsafe_allow_html=True)
