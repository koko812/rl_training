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
