---
name: ui-design-system
description: Design System para a interface do CRM e Landing Page, baseado no protótipo Figma. Define cores, tipografia, estilos de componentes e guidelines de UI.
---

# UI Design System - Casa de Repouso

Este documento serve como guia definitivo para a criação e atualização das interfaces do projeto, garantindo fidelidade ao protótipo aprovado no Figma.

## 1. Cores (Color Palette)
A paleta de cores foca no contraste aconchegante entre tons pastéis e cores quentes.

- **Bege Claro (Background Principal):** `#FFEED5` - Usado para o fundo geral do site e na maioria das seções de conteúdo. Traz a sensação de conforto.
- **Vermelho Escuro (Cor Primária/Marca):** `#7A1515` (Aprox. vinho/bordeaux) - Usado para os Títulos de Seção, Botões principais, faixas de "Graus de Dependência" e o Rodapé (Footer). Transmite firmeza e atenção.
- **Branco:** `#FFFFFF` - Fundo dos campos de texto do formulário e cor das letras sobre as faixas vermelho-escuras.
- **Cinza Claro/Médio:** Usado para placeholders de imagem e bordas e textos secundários.

## 2. Tipografia
- **Família da Fonte:** Sem serifa, limpa e moderna (ex: 'Inter', 'Roboto', 'Open Sans').
- **Headings (Títulos):** Devem usar o **Vermelho Escuro** e peso **Bold**. Os títulos devem atrair logo a atenção.
- **Corpo do Texto:** Cor escura para leitura focada, com linhas espaçadas adequadamente (`line-height: 1.5` ou maior).

## 3. Componentes

### Botões (Calls to Action)
- **Visual:** Fundo em **Vermelho Escuro**, formatação de borda arredondada (ex: `.rounded-md` ou `.rounded-lg` no Tailwind), texto claro em **Bold**.
- **Ações no Figma:** "Agende uma visita" e "Entre em contato".
- **Hover States:** Incluir uma sutil redução de luminosidade em mouse-over.

### Formulários (Inputs)
- **Visual:** Muito característico no Figma, os campos de entrada (Nome, Telefone, Select) possuem **bordas totalmente arredondadas** (estilo "pílula", `border-radius: 50px` ou `rounded-full`).
- **Fundo:** Fundo Branco (`#FFFFFF`) e contorno muito leve ou cinza claro.

### Seções de Serviços (Graus)
- **Blocos Sequenciais:** O Figma apresenta os Graus 1, 2 e 3 como faixas horizontais de ponta a ponta com cor de fundo **Vermelho Escuro** e textos em branco.
- Cada faixa possui o título do grau e uma breve descrição explicativa.

### Ícones
- Ícones de Contato (WhatsApp, Instagram, Localização) possuem estética *Outline* e usam a cor vermelha escura quando sobrepostos no fundo bege.

## 4. Estrutura de Layout e Espaçamentos
- **Mobile First:** O design reflete um layout empilhado (coluna única em telas menores), com amplos respiros (`padding`) superiores e inferiores em cada seção.
- **Header (Topo):** Fundo Bege, Logo estilizada à esquerda, Menu Hambúrguer à direita.
- **Hero Image:** A primeira dobra contém uma foto cobrindo toda a largura até o topo da seção seguinte.
- **Rodapé:** Bloco escuro com logo centralizada.

## 5. Diretrizes Práticas (Implementação)
1. **Sempre** aplique as cores exatas ou o mais próximo do visual quando estilizar o CSS.
2. Atualize o `style.css` para refletir os utilitários de cores (ex: `.bg-beige { background-color: #FFEED5; }`, `.text-brand { color: #7A1515; }`).
3. Para interfaces focadas em idosos e familiares, mantenha botões grandes, contraste de texto forte e leitura confortável.
