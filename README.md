# Context-Free-Grammar-Simulator

1. **Gramática Livre de Contexto**

  A implementação da gramática livre de contexto foi baseada em ideias do trabalho anterior. Representamos os símbolos terminais e não terminais cada um em conjunto, e um símbolo não terminal como símbolo inicial. As produções são constituídas de um lado esquerdo com um não terminal, e um lado direito com uma lista de símbolos; e são mantidas em um outro conjunto. São também implementadas funções de comparação e hash para podermos utilizar as produções de modo mais simples.

  Criamos estes objetos chamando um método estático que converte um texto para as novas instâncias. Este método é implementado de maneira bem genérica, considerando todos os símbolos que aparecem no lado esquerdo de uma produção como não terminais, e todos os outros como terminais. Um novo objeto que representa a gramática é criado com o símbolo inicial e os conjuntos de terminais e não terminais já configurados, então o conjunto de produções é populado.

  Temos também os métodos de first e follow. O first de uma sequência de símbolos é calculado da seguinte maneira: se o primeiro símbolo da sequência é um terminal, ele é retornado; se não(se o símbolo é um não terminal) o first das produções que tem esse não terminal como lado esquerdo são unidos em um único conjunto, se este conjunto contêm o símbolo épsilon ele ainda é unido com first do resto da sequência após o símbolo não terminal, este conjunto então é retornado. O follow de um símbolo não terminal é obtido deste modo: adicionados o símbolo $ no follow do símbolo inicial; então passamos por todos os lados direitos das produções identificando cada aparição de um não terminal, adicionamos o first do resto da sequência de símbolos ao follow deste não terminal, após analisar uma produção verificamos se o símbolo épsilon ficou no follow de algum não terminal, quando isso acontece adicionamos o símbolo não terminal do lado esquerdo da produção no follow deste não terminal; após isso, trocamos cada símbolo não terminal que aparece em um follow pelo seu follow(se A possui B em seu follow, o follow de B está contido no follow de A), realizamos isso até que todos os símbolos não terminais sejam retirados dos follows, retornamos o follow do não terminal que estamos interessados.

  Também é necessário checar se uma gramática é LL(1), realizamos isso através de 3 outros métodos: checar se há recursão à esquerda, checar se é fatorada à esquerda e checar se há conflito entre o first e o follow dos não terminais que levam para épsilon; estes métodos são baseados em chamadas dos métodos first e follow mencionados anteriormente. Há recursão à esquerda se verificamos que o método first entraria em recursão infinita. A gramática não é fatorada se um não terminal não é fatorado, e um não terminal não é fatorado se existe alguma intersecção entre os firsts de duas produções deste não terminal. E para a 3ª condição, primeiro identificamos os não terminais que levam a épsilon, destes verificamos se há alguma intersecação entre seu first e follow.
  
2. **Parser Descendente Recursivo**

  As instâncias do parser são inicialmente definidas apenas por uma gramática, que é verificada se é LL(1). Temos um método principal para a geração de código, que apenas concatena o código “main”(onde o parser começa a ser executado), o código do método que busca o próximo símbolo léxico e o código respectivo de cada não terminal. Outro método que realiza o reconhecimento de uma sentença, criando um novo escopo separado onde o código do parser é executado, repassando a sentença desejada para o método “main” nesse novo escopo e retornando o resultado.
  
  O método “main” configura algumas variáveis globais para este novo contexto, deixando a sentença a ser analisada e a posição atual disponível para os outros métodos; chama a pelo primeiro símbolo léxico e pelo método do símbolo inicial; na volta da recursão checa se o símbolo atual é o fim da sentença($). O método para buscar o próximo símbolo apenas incrementa um na posição atual e muda a variável global que contêm o símbolo atual.
  
  A construção do resto do parser é responsabilidade de outros três métodos: gerador de código de um símbolo, gerador de código de uma produção e gerador de código de um não terminal. Para gerar o código de um símbolo verificamos se ele é terminal então retornamos um trecho de código que testa se é o símbolo que esperamos e passa para o próximo símbolo, se não for o símbolo que esperamos joga uma exceção(“if x ==’a’: next_symbol() else raise exception”); se não for um terminal, então retornamos o trecho de código que chama pelo método do não terminal esperado(“A()”). Para gerar o código de uma produção fazemos uma simples concatenação dos trechos de código de cada um de seus símbolos e retornamos. E no gerador de código de não terminal o trecho de código define um novo método(“def A()”) com o nome igual ao do não terminal; é criado uma pequena seção para cada produção(onde o trecho de código da produção é colocado), tal para entrar em certa seção é necessário que o símbolo atual esteja no first daquela produção; ainda se este não terminal não possuir épsilon em seu first é criado uma última seção “else” que joga uma exceção(pois o não terminal foi chamado mas nenhuma das suas produções foi seguida).
  
3. **Interface Gráfica**

  A GUI foi feita utilizando o framework Qt e possui os seguintes elementos:
  
  1. *Edição, leitura e gravação de gramáticas*
  
    Uma caixa de texto onde a gramática pode ser editada. Um botão para abrir um arquivo tal que o conteúdo deste arquivo é colocado na caixa de edição de gramática; e um botão que possibilita salvar o conteúdo atual da caixa de texto em um arquivo. A leitura e gravação de arquivos é mostrada no log.

  2. *Verificação da propriedade LL(1) na gramática atual e conversão para parser descendente recursivo*
	
	  Um botão para verificar a propriedade LL(1) da gramática atual, os resultados são mostrados no log e em uma nova janela; mostrando detalhes de problemas de recursão, não fatoração ou conflito first/follow. Outro botão para realizar a conversão da gramática para parser descendente recursivo, a verificação de LL(1) também é realizada e seus resultados também são mostrados, assim como as sub-operações para criação do código do parser; o código final do parser é mostrado numa segunda caixa de texto, maior para melhorar a visualização.

  3. *Visualização do código do parser e reconhecimento de sentenças*
  
    O código do parser atual pode ser visualizado em uma caixa de texto junto à um campo onde uma sentença pode ser inserida para ser verificada se é reconhecida pelo parser. Os detalhes do reconhecimento também são mostrados no log e em caixas de texto.

    Log das operações e sub-operações realizadas e seus resultados, e limpeza do log
  
    Uma terceira caixa de texto mostra todas as operações e sub-operações realizadas e seus resultados para facilitar a verificação dos procedimentos. E ainda um botão para limpar o log para melhorar a visualização das operações.
