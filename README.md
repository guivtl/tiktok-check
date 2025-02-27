# 🔍 TikTok Block Checker

Um bot em Python que monitora e notifica quando usuários do TikTok removem o bloqueio do seu perfil, enviando notificações via Telegram com screenshots.

## ⭐ Funcionalidades

- ✅ Verificação automática de status de bloqueio
- 📱 Notificações instantâneas via Telegram
- 📸 Screenshots automáticos como evidência
- 🔐 Sistema de login com cookies persistentes
- 🤖 Resolução automática de captchas
- 🎨 Interface CLI amigável e colorida
- 🏃 Modo headless (execução em background)
- ⏱️ Intervalos aleatórios entre verificações

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Google Chrome
- Conexão com internet
- Conta no TikTok
- Bot do Telegram
- Chave API do SadCaptcha

## 🚀 Instalação

1. Clone o repositório:

```     
git clone https://github.com/seu-usuario/tiktok-block-checker.git
cd tiktok-block-checker
```

2. Execute o arquivo `start.bat` ou instale manualmente as dependências:

```
pip install -r requirements.txt
```

3. Configure o arquivo `config.json`:
```
{
    "sadcaptcha_api_key": "sua_chave_api_sadcaptcha",
    "telegram_bot_token": "seu_token_bot_telegram",
    "telegram_chat_id": "seu_chat_id_telegram"
}
```

## 🔑 Obtendo as Credenciais

### SadCaptcha API
1. Crie uma conta em [SadCaptcha](https://sadcaptcha.com)
2. Acesse o painel e gere sua chave API
3. Copie a chave para o `config.json`

### Bot do Telegram
1. Converse com [@BotFather](https://t.me/botfather)
2. Use `/newbot` para criar um novo bot
3. Copie o token fornecido
4. Inicie uma conversa com seu bot
5. Acesse: `https://api.telegram.org/bot<SEU_TOKEN>/getUpdates`
6. Envie uma mensagem para o bot
7. Copie o `chat_id` da resposta JSON

## 📱 Como Usar

### Primeiro Acesso (Login)

python app.py

1. Escolha opção 1
2. Faça login no TikTok na janela que abrir
3. Aguarde a confirmação de salvamento dos cookies

### Monitorar Usuários

```
python app.py
```

1. Escolha opção 2
2. Digite o @ do usuário a ser monitorado
3. O bot iniciará a verificação automática

## ⚙️ Como Funciona

1. O bot usa os cookies salvos para acessar o TikTok
2. Verifica periodicamente o perfil do usuário alvo
3. Detecta mudanças no status de bloqueio
4. Ao detectar desbloqueio:
   - Captura screenshot da página
   - Envia notificação via Telegram
   - Continua monitorando

## ⚠️ Notas Importantes

- Mantenha suas credenciais seguras
- Use o bot de forma responsável
- Respeite os limites de requisições do TikTok
- Não compartilhe seus cookies
- Evite múltiplas instâncias simultâneas

## 🔧 Solução de Problemas

### Erro nos Cookies
- Apague o arquivo `tiktok_cookies.json`
- Execute a opção 1 novamente

### Falha no Captcha
- Verifique sua chave SadCaptcha
- Confirme se há créditos disponíveis

### Problemas no Telegram
- Verifique se o bot está ativo
- Confirme o chat_id
- Teste o token manualmente


## 👥 Contribuindo

1. Faça um Fork
2. Crie sua branch (`git checkout -b feature/NovaFuncionalidade`)
3. Commit suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- Abra uma issue para reportar bugs
- Use Discussions para dúvidas
- Sugestões são bem-vindas

## 🔗 Links Úteis

- [Selenium Docs](https://www.selenium.dev/documentation/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [SadCaptcha](https://www.sadcaptcha.com/api/v1/swagger-ui/index.html)
