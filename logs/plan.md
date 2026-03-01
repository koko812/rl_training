# 🧱 Phase 1：Policy Gradient の身体化（1〜2週間）

目的：

* logprob × reward の意味を完全理解
* entropy / baseline / KL の役割を体感

---

## 🔹 1-1 Multi-armed Bandit（状態なし）

やること：

* 3〜5アーム
* softmax(logits) 直接最適化
* REINFORCE 実装

見るもの：

* アーム確率の推移
* reward scale を変えたときの挙動
* baseline あり/なしの分散差
* entropy係数を変えたときの探索

これで

> 「分布を歪める」という感覚を掴む

---

## 🔹 1-2 Contextual Bandit（線形）

やること：

* x ∈ ℝ²
* 3アーム
* 線形 policy

見るもの：

* 入力空間での決定境界
* entropy の役割
* explorationの必要性

ここで

> π(a|x) の幾何を理解

---

# 🧠 Phase 2：協調の最小模型（2〜3週間）

目的：

* 非定常性
* credit assignment
* 通信の必要性

---

## 🔹 2-1 Sender–Receiver ゲーム

設定：

* A は半分の情報を見る
* B は残りを見る
* A → メッセージ → B
* 共有報酬

やること：

* 同時学習 vs 交互学習
* entropy を変える
* baseline を入れる

見るもの：

* 通信が成立する瞬間
* collapse する瞬間
* 同時学習の不安定性

---

## 🔹 2-2 Tool-use Bandit

設定：

* Reasoner が最終選択
* Domain がアドバイス
* 問い合わせにコスト

見るもの：

* 「聞く/聞かない」の境界
* 信頼度の学習
* cost と KL の関係

ここは LLM協調に直結。

---

# 🔥 Phase 3：分布協調（あなたの独自領域）

目的：

* 複数分布の融合を理解

---

## 🔹 3-1 Logit Fusion 実験（banditで）

* 2エージェントがそれぞれ logits 出す
* 合議ルールを変える

  * 平均
  * 加重平均
  * KL制御
  * gatingネットワーク

見るもの：

* 分布の形の変化
* entropyの変化
* collapse条件

---

## 🔹 3-2 同時更新 vs 交互更新

* 両者 policy gradient
* 同時に更新
* 交互に更新

観察：

* どちらが安定？
* KLがどこで効く？

---

# 🚀 Phase 4：LLMへ戻す

ここで初めて：

* 小さなモデル
* format遵守
* tool-call gating
* dual-model decoding

へ戻す。

このとき：

> あ、banditと同じだ

という感覚が出るはず。

---

# 🎯 優先順まとめ

### Step 1（必須）

Bandit + baseline + entropy + KL

### Step 2（重要）

Contextual Bandit

### Step 3（核心）

Sender–Receiver

### Step 4（あなたの武器）

Logit-level fusion
