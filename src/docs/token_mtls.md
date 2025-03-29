Token para gerar certificado mTLS

Este endpoint permite obter um token de acesso para gerar o certificado mTLS.

Aplicação de scopes:
Para maior segurança, nossas APIs utilizam scopes, que servem para limitar o acesso dos tokens. Ao utilizá-los, você define a quais funcionalidades o token gerado terá acesso.
Você poderá utilizar até dez scopes para cada token gerado, separados por um espaço em branco, conforme demonstrado a seguir:
Exemplo: scope="kyc.document.write business.write boleto.read"

Dica:
Para conhecer todos os scopes suportados, acesse a página Scopes.

Pré-requisito:
Para que seja possível utilizar este endpoint, é necessário que:
- O parceiro tenha recebido as credenciais de sandbox (client_id e client_secret).

Recebimento de credenciais de sandbox:
Para que o parceiro possa realizar os testes em nossas APIs, o time de TAM fornecerá as credenciais de autorização de sandbox (compostas por client_id e client_secret), logo após o Kickoff de Projetos.
Ao informar o seu client_id e client_secret em nosso endpoint, disponibilizaremos um token de acesso baseado no protocolo de autorização OAuth2.

Atenção:
O vazamento das suas informações de acesso pode causar inúmeras fraudes. Guarde-as em um lugar seguro! Caso ocorra algum problema com os seus dados de autorização, entre em contato imediatamente com o time de TAM.

Requisição (Request):
Requisição HTTP (cURL):
POST https://login.sandbox.bankly.com.br/connect/token

Autorização:
Esta requisição requer o scope descrito a seguir:
Scope: certificate.create – Concede acesso para emitir e baixar o certificado para mTLS.

Cabeçalhos (Headers):
Content-Type: Obrigatório. Tipo de dado que o arquivo contém. Neste caso, application/x-www-form-urlencoded.

Parâmetros da rota (Path):
Não é necessário enviar parâmetros no path desta requisição.

Corpo da requisição (Body):
No body, envie os seguintes campos em formato x-www-form-urlencoded:
- grant_type (string): Obrigatório. Método pelo qual suas aplicações podem obter tokens de acesso. Informe o valor client_credentials.
- client_id (string): Obrigatório. Identificador público de sua aplicação. Valor fornecido pelo time de Implantação. Formato UUID v4.
- client_secret (string): Obrigatório. Segredo conhecido por sua aplicação e pelo servidor de autorização. Valor fornecido pelo time de TAM.
- scope (string): Obrigatório. Scope da API que deseja acessar. Você poderá utilizar até dez scopes para cada token gerado. Os scopes devem estar separados por um espaço em branco. Exemplo: "kyc.document.write business.write boleto.read".

Exemplo de corpo:
grant_type=client_credentials
&client_id={{yourClientId}}
&client_secret={{yourClientSecret}}
&scope={{yourScope}}

Resposta (Response):
O status code 200 indicará sucesso na criação do token.
Sendo bem-sucedido, o retorno trará os seguintes campos em formato JSON:
- access_token (string): Token gerado.
- expires_in (integer): Tempo de expiração do token. O valor padrão é 3600.
- token_type (string): Tipo de token. Nesse caso, "Bearer".
- scope (string): Scopes dos produtos em que o token poderá ser utilizado.

Exemplo de resposta JSON:
{
    "access_token": "[yourAccessToken]",
    "expires_in": 3600,
    "token_type": "Bearer",
    "scope": "[yourScope]"
}

Nota:
Não é necessário gerar um token por requisição. Utilize o campo expires_in para verificar a validade do token.

Dica:
Para simular uma requisição nesse endpoint, acesse o API Reference.

Erros:
Este endpoint não retorna erros específicos. Porém, ele poderá retornar alguns erros comuns entre todos os endpoints.