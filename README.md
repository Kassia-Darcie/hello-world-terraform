## Contribuindo com o projeto

### Convenção de nomenclatura de branches

Para manter a organização, utilize a seguinte convenção para nomear branches:

-   `feature/nome-da-branch`: Desenvolvimento de novas funcionalidades
-   `bugfix/nome-do-bug`: Correção de bugs
-   `hotfix/nome-do-hotfix`: Correção urgente em produção
-   `release/x.y.z`: Lançamento de um novo release

**Regras Adicionais:**

-   Use apenas letras minúsculas.
-   Use hifens (`-`) para separar palavras.
-   Não utilize caracteres especiais ou espaços.

### Abertura de Pull Requests (PRs)

Pull Requests (ou Merge Requests) são a forma de propor suas mudanças para serem revisadas e integradas na branch principal.

### Antes de Abrir um PR

1.  **Certifique-se de que sua branch está atualizada** com a branch principal (geralmente `main` ou `dev`). Use `git pull origin <branch-base>` e resolva conflitos se houver.
2.  **Faça commits atômicos** e com mensagens claras, seguindo a convenção de [Conventional Commits](#convenção-de-commits).

-   **Use `merge`:** Para integrar branches de feature/bugfix na branch principal (`main`/`dev`) **após a revisão do PR**. **Sempre use merge para integrar branches que já foram publicadas e que outros podem ter baseado trabalho.**
-   **Use `rebase`:** Para manter sua branch de trabalho (`feature/`, `bugfix/`, etc.) atualizada com a branch principal (`main`/`dev`) **ANTES de abrir um PR**. Isso mantém seu histórico limpo e facilita a revisão. **Nunca use rebase em branches que já foram publicadas e que outros podem estar usando.**

### Convenção de commits

Mensagens de commit claras e consistentes são vitais para rastrear o histórico do projeto, gerar changelogs e entender as mudanças. Adotamos a convenção de **Conventional Commits**.

**Tipos de Commit Comuns:**

-   `feat`: Uma nova funcionalidade.
-   `fix`: Uma correção de bug.
-   `docs`: Mudanças na documentação.
-   `style`: Mudanças que não afetam o significado do código (espaços em branco, formatação, ponto e vírgula ausente, etc.).
-   `refactor`: Uma mudança de código que não corrige um bug nem adiciona uma funcionalidade.
-   `perf`: Uma mudança de código que melhora a performance.
-   `test`: Adição ou correção de testes.
-   `chore`: Mudanças no processo de build, ferramentas auxiliares, bibliotecas externas, etc. (não afeta o código de produção).
-   `build`: Mudanças que afetam o sistema de build ou dependências externas (npm, webpack, etc.).
-   `ci`: Mudanças nos arquivos e scripts de configuração de CI.
