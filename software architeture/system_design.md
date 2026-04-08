# System Design

System Design é o processo de definir a arquitetura, os componentes, as interfaces e os fluxos de um sistema de software de forma a atender requisitos funcionais e não funcionais. Diferente de aprender conceitos isolados, System Design exige a capacidade de integrar múltiplos conhecimentos — como escalabilidade, consistência, concorrência, resiliência e observabilidade — para construir soluções que funcionem sob condições reais de produção.

O ponto de partida de qualquer system design é a compreensão clara dos requisitos. Requisitos funcionais definem o que o sistema deve fazer, enquanto requisitos não funcionais definem como o sistema deve se comportar, incluindo desempenho, disponibilidade, escalabilidade, segurança e custo. Muitos erros de arquitetura acontecem não por falta de conhecimento técnico, mas por não entender corretamente o problema que precisa ser resolvido.

Após entender os requisitos, o próximo passo é definir a arquitetura de alto nível. Isso envolve identificar os principais componentes do sistema, como serviços, bancos de dados, filas e caches, e como eles interagem. Nesse estágio, decisões importantes são tomadas, como escolher entre monolito ou microserviços, comunicação síncrona ou assíncrona, e tipos de armazenamento de dados.

Um dos aspectos mais críticos do system design é a escalabilidade. O sistema deve ser capaz de lidar com aumento de carga ao longo do tempo. Isso envolve decisões como uso de horizontal scaling, load distribution e particionamento de dados. Escalar leitura é relativamente simples com réplicas, mas escalar escrita exige estratégias mais complexas, como sharding e controle de consistência.

A consistência de dados é outro ponto central. Em sistemas distribuídos, é necessário decidir entre consistência forte e eventual, considerando os trade-offs definidos pelo CAP theorem. Essa decisão impacta diretamente a complexidade do sistema, a experiência do usuário e a tolerância a falhas.

Concorrência também desempenha um papel fundamental. O sistema precisa lidar com múltiplas operações simultâneas sem comprometer a integridade dos dados. Isso envolve o uso de mecanismos como optimistic locking, pessimistic locking e controle de transações. Problemas como race conditions e lost updates precisam ser considerados desde o design.

A resiliência é outro pilar essencial. Sistemas reais precisam continuar funcionando mesmo diante de falhas. Isso envolve o uso de padrões como retry com backoff, circuit breaker, throttling e dead letter queues. O objetivo é evitar falhas em cascata e permitir recuperação controlada.

A comunicação entre componentes é uma decisão importante. Comunicação síncrona, como chamadas HTTP, é mais simples, mas pode introduzir acoplamento e latência. Comunicação assíncrona, baseada em filas e eventos, melhora desacoplamento e escalabilidade, mas aumenta complexidade e dificulta rastreamento.

O gerenciamento de dados também é uma parte crítica do system design. A escolha entre SQL e NoSQL depende de requisitos de consistência, volume de dados e padrões de acesso. Além disso, estratégias de cache são frequentemente utilizadas para melhorar performance, reduzindo carga em sistemas downstream.

Observabilidade é essencial para operar sistemas em produção. Sem métricas, logs e traces, é impossível entender o comportamento do sistema ou diagnosticar problemas. System design deve incluir desde o início estratégias de monitoramento e análise.

Outro aspecto importante é o controle de carga. Sistemas precisam lidar com picos de tráfego sem falhar. Técnicas como rate limiting, throttling e backpressure ajudam a proteger o sistema contra sobrecarga.

O design também deve considerar deployment e evolução. Sistemas precisam ser atualizados sem downtime, utilizando estratégias como rolling updates e canary releases. Além disso, o design deve permitir evolução gradual, evitando acoplamento excessivo.

Em entrevistas de system design, o objetivo não é encontrar uma única solução correta, mas demonstrar capacidade de raciocínio, entendimento de trade-offs e habilidade de justificar decisões. Um bom design não é aquele que resolve todos os problemas, mas aquele que equilibra corretamente as necessidades do sistema.

Um erro comum é tentar otimizar tudo desde o início. System design deve ser iterativo. Começa-se com uma solução simples e evolui conforme a necessidade. Premature optimization pode levar a complexidade desnecessária.

Outro ponto importante é que system design é altamente contextual. A melhor solução depende do tipo de sistema, escala, requisitos de negócio e restrições técnicas. Não existe arquitetura universalmente correta.

Em termos práticos, system design envolve constantemente tomar decisões baseadas em trade-offs. Melhorar consistência pode reduzir disponibilidade. Aumentar escalabilidade pode aumentar complexidade. Reduzir latência pode aumentar custo. Entender esses trade-offs é o que diferencia um engenheiro iniciante de um engenheiro experiente.

Em resumo, system design é a disciplina de projetar sistemas completos que atendem requisitos reais de forma eficiente, escalável e resiliente. Ele integra todos os conceitos de arquitetura e exige pensamento crítico, capacidade de abstração e tomada de decisão baseada em trade-offs.