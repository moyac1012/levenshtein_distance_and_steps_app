from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def levenshtein_distance_and_steps(S, T):
    m, n = len(S), len(T)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if S[i - 1] == T[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    
    i, j = m, n
    steps = []
    simulation = [S]  # 変化の過程を保存するリスト

    while i > 0 or j > 0:
        if i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            steps.append(f"削除: {S[i - 1]} (位置 {i - 1})")
            S = S[:i - 1] + S[i:]  # 文字列から削除
            simulation.append(S)
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            steps.append(f"追加: {T[j - 1]} (位置 {j - 1})")
            S = S[:i] + T[j - 1] + S[i:]  # 文字列に追加
            simulation.append(S)
            j -= 1
        else:
            if S[i - 1] != T[j - 1]:
                steps.append(f"置換: {S[i - 1]} → {T[j - 1]} (位置 {i - 1})")
                S = S[:i - 1] + T[j - 1] + S[i:]  # 文字列を置換
                simulation.append(S)
            i -= 1
            j -= 1

    steps.reverse()
    simulation.reverse()

    return dp[m][n], steps, simulation

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    S1 = data['S1']
    S2 = data['S2']
    distance, steps, simulation = levenshtein_distance_and_steps(S1, S2)
    return jsonify({'distance': distance, 'steps': steps, 'simulation': simulation})

if __name__ == '__main__':
    app.run(debug=False)
