import sys
import os
import urllib.request
import urllib.error

def install_skill(repo, skill_path):
    """
    Realiza o download sob demanda de uma skill específica de um repositório no GitHub.
    Exemplo: python skill_manager.py install alirezarezvani/claude-skills marketing-skill/seo-expert
    """
    print(f"Buscando skill '{skill_path}' do repositório '{repo}'...")
    
    # Assume branch main, caso não seja, pode ser passado como parâmetro no futuro
    branch = "main"
    raw_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{skill_path}/SKILL.md"
    
    # O diretório de destino local será .agent/skills/<ultimo_nome_da_pasta>
    skill_name = os.path.basename(skill_path.strip('/'))
    # Identificando a base do projeto mcp (assumindo que o script roda sempre em mcp/.agent/scripts/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.abspath(os.path.join(script_dir, "..", "skills", skill_name))
    
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, "SKILL.md")
    
    try:
        print(f"Fazendo download de: {raw_url}")
        req = urllib.request.Request(raw_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            
        with open(target_file, "w") as f:
            f.write(content)
            
        print(f"✅ Skill '{skill_name}' salva com sucesso em: {target_file}")
    except urllib.error.HTTPError as e:
        print(f"❌ Erro HTTP {e.code}: O arquivo não existe nesse caminho ou o repositório é privado.")
    except Exception as e:
        print(f"❌ Erro fatal ao tentar baixar a skill: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python skill_manager.py install <org/repo> <skill_folder_path>")
        print("Exemplo: python skill_manager.py install alirezarezvani/claude-skills engineering/startup-cto")
        sys.exit(1)
    
    command = sys.argv[1]
    repo_arg = sys.argv[2]
    skill_arg = sys.argv[3]
    
    if command == "install":
        install_skill(repo_arg, skill_arg)
    else:
        print(f"Comando desconhecido: {command}")
