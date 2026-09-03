from routers.auth_routes import auth_router
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routers.order_routes import order_router

app = FastAPI(title="API de Gerenciamento de Pedidos")

app.include_router(auth_router)
app.include_router(order_router)


# --- HOMEPAGE NATIVA DA API ---
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def homepage():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API de Gerenciamento de Pedidos</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-slate-100 font-sans antialiased">
        <main class="max-w-4xl mx-auto p-8 space-y-6 flex flex-col items-center">
            
            <h1 class="text-3xl font-bold text-blue-400 mt-4 text-center">
                🚀 API de Gerenciamento de Pedidos
            </h1>
            <p class="text-slate-400 text-center text-lg">
                Painel inicial da aplicação. Utilize os links e a tabela abaixo para navegar na API.
            </p>

            <!-- Botões para Swagger e ReDoc -->
            <div class="flex gap-4 my-2">
                <a href="/docs" class="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-lg font-medium transition flex items-center gap-2">
                    📄 Abrir Swagger UI
                </a>
                <a href="/redoc" class="bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-4 py-2 rounded-lg font-medium transition flex items-center gap-2">
                    📚 Abrir ReDoc
                </a>
            </div>

            <!-- Aviso de Autenticação -->
            <div class="w-full bg-slate-800 border border-slate-700 p-4 rounded-lg space-y-2">
                <h2 class="text-lg font-bold text-amber-400">🔒 Autenticação Necessária</h2>
                <p class="text-sm text-slate-300">As rotas de pedidos requerem o token JWT no cabeçalho:</p>
                <div class="bg-slate-950 p-2 rounded text-emerald-400 font-mono text-sm">
                    Authorization: Bearer &lt;seu_token&gt;
                </div>
            </div>

            <!-- Tabela de Rotas -->
            <div class="w-full">
                <h2 class="text-xl font-bold text-slate-200 mb-4">📌 Resumo das Rotas</h2>
                <div class="overflow-x-auto border border-slate-700 rounded-lg">
                    <table class="w-full text-left text-sm text-slate-300">
                        <thead class="bg-slate-800 text-slate-200 font-mono uppercase text-xs border-b border-slate-700">
                            <tr>
                                <th class="p-3">Método</th>
                                <th class="p-3">Rota</th>
                                <th class="p-3">Descrição</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800 bg-slate-800/50">
                            <tr><td class="p-3 text-emerald-400 font-bold font-mono">GET</td><td class="p-3 font-mono">/pedidos/</td><td class="p-3">Teste de conexão e acesso</td></tr>
                            <tr><td class="p-3 text-blue-400 font-bold font-mono">POST</td><td class="p-3 font-mono">/pedidos/pedido</td><td class="p-3">Criar um novo pedido</td></tr>
                            <tr><td class="p-3 text-blue-400 font-bold font-mono">POST</td><td class="p-3 font-mono">/pedidos/pedido/adicionar-item/{id}</td><td class="p-3">Adicionar item ao pedido</td></tr>
                            <tr><td class="p-3 text-blue-400 font-bold font-mono">POST</td><td class="p-3 font-mono">/pedidos/pedido/remover-item/{id}</td><td class="p-3">Remover item do pedido</td></tr>
                            <tr><td class="p-3 text-blue-400 font-bold font-mono">POST</td><td class="p-3 font-mono">/pedidos/pedido/cancelar/{id}</td><td class="p-3">Cancelar um pedido</td></tr>
                            <tr><td class="p-3 text-blue-400 font-bold font-mono">POST</td><td class="p-3 font-mono">/pedidos/pedido/finalizar/{id}</td><td class="p-3">Finalizar um pedido</td></tr>
                            <tr><td class="p-3 text-emerald-400 font-bold font-mono">GET</td><td class="p-3 font-mono">/pedidos/pedido/{id}</td><td class="p-3">Visualizar detalhes do pedido</td></tr>
                            <tr><td class="p-3 text-emerald-400 font-bold font-mono">GET</td><td class="p-3 font-mono">/pedidos/listar/pedidos-usuario</td><td class="p-3">Listar meus pedidos</td></tr>
                            <tr><td class="p-3 text-emerald-400 font-bold font-mono">GET</td><td class="p-3 font-mono">/pedidos/listar</td><td class="p-3">Listar todos (Apenas Admin)</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

        </main>
    </body>
    </html>
    """