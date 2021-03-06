# Deferred-Acceptanceアルゴリズム

[安定結婚問題](https://ja.wikipedia.org/wiki/%E5%AE%89%E5%AE%9A%E7%B5%90%E5%A9%9A%E5%95%8F%E9%A1%8C)や大学選択問題を解くDeferred-Acceptanceアルゴリズム（Gale-Shapleyアルゴリズム）を実装してみる。

## 現状
1対1のDAアルゴリズムは完成。

要求仕様: https://github.com/OyamaZemi/exercises2015/tree/master/ex02  
実行結果: https://github.com/13tsuyoshi/DA_algorithms/blob/master/DA_Algorithms.ipynb


### 今後簡単にできそうなこと

* DAアルゴリズムから出てきたマッチングが、本当にStableかを確かめる（Blocking Pairが無いことを確かめる）関数を作る
* apply側の申し込み順を入れ替えても、結果は変わらないことを確かめる
* apply側とhost側の効用（人数n - マッチングした相手の順位k）を計算する関数を作る
* DAアルゴリズムがapply側の効用を最大化（host側の効用を最小化）していることを確かめる
* apply側に虚偽申告をするインセンティブが無い一方、host側には虚偽申告をするインセンティブがあることを確かめる
* 不完全な選好表に対応する
* 多対1のDAアルゴリズムの実装

### 難しそうなこと

* Stable Matchingを全出力する関数を作る（指数オーダらしい）
* 男女の効用和を最大化 / 効用差を最小化するマッチングを考える
* 同順を許した選好に対応する（進振りにおいて、学部は点数の同じ学生に優劣を付けないはず）



## 文献

### Paperと本

※以下にあるPaperは全て[SSL-VPN Gateway](https://gateway.itc.u-tokyo.ac.jp/dana-na/auth/url_default/welcome.cgi)を使って（学外からでも）読める。

* _D. Gale and L.S. Shapley, "[College Admissions and the Stability of Marriage](http://www.jstor.org/stable/2312726)," American Mathematical Monthly 69 (1962), 9-15_  
元論文。安定結婚問題（1対1）、学校選択問題（多対1）の定式化、GSアルゴリズムの導入・安定マッチングを必ず求められることの証明  


* _A.E. Roth, "[Deferred Acceptance Algorithms: History, Theory, Practice, and Open Questions](http://link.springer.com/article/10.1007/s00182-008-0117-6)," International Journal of Game Theory 36 (2008), 537-569_  
DAアルゴリズムのいろいろ（？）


* _坂井豊貴・藤中裕二・若山琢磨『メカニズムデザイン -資源配分制度の設計とインセンティブ-』(2008) ミネルヴァ書房_  
第7章で安定結婚問題(1対1)におけるGSアルゴリズムについて詳しく（証明付きで）解説されている。また、apply側が虚偽の選好を表明するインセンティブを持たないこと、一方host側はそれを持つことが示されている。多対1マッチングについては少しだけ。  


* _小島武仁・安田洋祐「マッチング・マーケットデザイン」『経済セミナー』2009年4・5月号_  
研修医マッチングと学校選択の話。DAアルゴリズムについての詳しい解説有。研修医マッチングのパートは[研修医マッチングの経済学 - ECONO斬り！！](http://blog.livedoor.jp/yagena/archives/50536286.html)にある。  


* _Robert W. Irving, David F. Manlove and Gregg O’Malley, "[Stable Marriage with Ties and Bounded Length Preference Lists](http://dcs.gla.ac.uk/publications/PAPERS/8279/SMTI-bounded.pdf)," Department of Computing Science, University of Glasgow, Glasgow G12 8QQ, UK._  
安定結婚問題で選好順位にタイを認めたり、不完全な選好リスト（こいつとだけは絶対ペアになりたくない！）を許した時の計算時間について  

* _柳澤弘揮・宮崎修一・岩間一雄 「[片方のみがタイを持つ安定結婚問題に対する25/17 近似アルゴリズム](http://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1691-21.pdf)」 『数理解析研究所講究録』第1691巻 (2010), 136-141頁_  
序章に、タイと不完全なリストを認めた場合の計算量の問題と近似アルゴリズムの話題が簡単に書かれている  


### Webページ

* _[経済学で理想のパートナーを探そう！ - ゲール＝シャプレーアルゴリズムを合コンのマッチング問題から考える](http://toyokeizai.net/articles/-/11584)_  
安定結婚問題（1対1）におけるGSアルゴリズムのわかりやすい解説。  


* _[安定マッチング - 各種アルゴリズムの C++ による実装](http://www.prefield.com/algorithm/misc/stable_matching.html)_  
GSアルゴリズムに加えて、それ以外の安定マッチング（男女の効用の和を最大にするマッチング、男女の効用差を最小にするマッチング）についても解説されている。タイや不完全なリストを許した時の具体的な実装に関するヒントも有。  


* _[Introduction to Market Design and Two-Sided Matching Markets](https://docs.google.com/viewer?a=v&pid=sites&srcid=ZGVmYXVsdGRvbWFpbnxmdWhpdG9rb2ppbWFlY29ub21pY3N8Z3g6NmVkYWU1ZGU5NDZkMWZh)_  
Fuhito Kojima先生の（授業?）スライド。  




