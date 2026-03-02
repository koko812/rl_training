# Learned Notes (2026-03-02)

## Multi-Bandit（基本）
- reward は環境が返す。**policy は action だけ返す**設計が綺麗。
- reward をグローバルにせず、環境の返り値として受け取る。

流れ（最小構成）:
```text
action = policy(...)
reward = env_step(action)
update(...)
```

## 入力処理
- `try/except` は **型変換**と**範囲チェック**の両方を入れる。
- `ValueError` は入力ミス専用で拾い、`Exception` は別扱いにする。

## サンプリング
- `random.random()` で Bernoulli（0/1）を閾値判定で生成。
- 重み付きサンプルは `random.choices(population, weights, k=1)`。

メモ（イメージ）:
```text
u = random.random()  # 0〜1
reward = 1 if u < p else 0
```

## Softmax
- 分子も分母も `exp(a)` を使う。
- 数値安定性が必要なら max を引く。

イメージ:
```text
probs_i = exp(logit_i - max_logit) / sum_j exp(logit_j - max_logit)
```

## Policy Gradient 更新（Bandit）
- `probs` は softmax 後の確率。更新対象は logits。
- logits と probs を混ぜるのは標準的で正しい。
- baseline で分散が下がる。まず baseline なしで挙動確認→その後比較。

更新方向のイメージ:
```text
delta = (reward - baseline) * (one_hot(action) - probs)
logits += lr * delta
```

## One-Hot / 配列演算
- Python の `list * scalar` は繰り返しになる（要素ごとの掛け算ではない）。
- one-hot は 0 埋め配列を作って index を 1 にする。

## Contextual Bandit（線形）
### 何が変わるか
- 各ターン「状態」`x` が与えられる。
- **行動は必ず実行される**が、当たりやすさが状態で変化する。
- つまり `p(reward=1 | a, x)` が `x` によって変わる。

### 最小の設定（線形）
- `x` は毎ターン独立にサンプル（例: `R^2` の正規/一様）。
- 各アームに重み `w_a` を持つ。
- 例: `p(reward=1 | a, x) = sigmoid(w_a · x)` のように線形で確率が変わる。

### 流れ（環境側の役割）
```text
x = sample_state()
action = policy(x)
p = reward_prob(action, x)
reward = sample_bernoulli(p)
```

### 具体例（線形でわかりやすいもの）
- 広告配信:
  - 状態 `x`: ユーザー特徴（年齢・興味）
  - 行動: 表示する広告
  - 当たりやすさ: ある特徴が大きいほど特定広告が当たりやすい
- レコメンド:
  - 状態 `x`: 直近の閲覧履歴の要約ベクトル
  - 行動: 推薦するカテゴリ
  - 当たりやすさ: ある方向の特徴が強いほどクリック確率が上がる
- A/B テスト:
  - 状態 `x`: 流入元・時間帯
  - 行動: 文面A/B/C
  - 当たりやすさ: 時間帯に応じて線形に変化

### 直感
- 「同じアームでも、状況によって当たりやすさが変わる」。
- だから **状態を見てアームを選ぶ**必要がある。

## NN が必要になる最小ケース
- 状態と報酬確率の関係が **非線形**（XOR・円形・島構造など）。
- 線形モデルでは分離できず、小さな NN が必要。

## 現実例の感覚
- 広告配信: ユーザー特徴でクリック確率が変わる。
- ギャンブル直感: 観測できる特徴が当たり確率を変える。

## Bandit と MDP の違い（倒立振り子・迷路の位置づけ）
- bandit は **1ステップ完結**で状態遷移がない。
- MDP は **行動が次の状態を変える**ため連鎖する。
- 遅延報酬・信用割当が本質的に難しくなるのは MDP。

## 遅延報酬を bandit に寄せると？
- 報酬を「最後だけ観測」にすると遅延感は出る。
- ただし **状態遷移がない限り bandit の延長**。
- MDPっぽさを出すには「行動が次の状態を変える」要素が必要。

## 強化学習が本領を発揮する条件
- 行動が未来の状態を変える（連鎖する意思決定）。
- 報酬が遅れて返ってくる（信用割当が必要）。
- 正解ラベルがなく、やった結果しか見えない（反実仮想が欠ける）。
- 探索が必要（試さないと分からない）。

## REINFORCE とは
- 最も基本的な **policy gradient**。
- 直感: 「良い報酬を得た行動の確率を上げる」。

更新の最小イメージ:
```text
delta = (reward - baseline) * (one_hot(action) - probs)
logits += lr * delta
```

## Policy Gradient と Q-learning の違い
- **Policy Gradient**: 確率 `π(a|s)` を直接最適化。
- **Q-learning**: 価値 `Q(s,a)` を学習して `argmax` で行動。
- 離散行動でも policy gradient は普通に使う（むしろ自然）。

直感の違い:
```text
Policy Gradient: 分布を滑らかに歪める
Q-learning: 価値差が出ると特定行動に寄りやすい
```

## どっちを使うかの実務的な目安
- 離散・決定的に近い最適行動が欲しい → Q-learning 系。
- 確率的・連続・分布操作が目的 → Policy Gradient 系。

## A2C が効く場面
- REINFORCE の分散が大きくて学習が不安定なとき。
- 遅延報酬のある MDP（迷路・倒立振り子など）で効果が出やすい。
- 価値関数（baseline）で分散を抑えて安定させる。
