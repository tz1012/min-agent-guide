---
type: guide
description: Version-aware OmO Native setup and proactive operation, distinguished from the OpenCode and Codex editions.
author:
  - Codex
date created: 2026-10-28
date modified: 2026-10-28
status: reference-verified-runtime-unverified
aliases: []
tags:
  - ai-agent
  - build-package
---

# OmO를 사용할 경우

여기서 OmO는 **code-yeongyu/oh-my-openagent의 OmO Native**를 뜻한다고 가정한다. 2026-10-28 공식 README는 독립 `omo` 명령과 `omo-ai` 패키지를 안내하며, OpenCode 플러그인과 Codex/Light edition은 별도다. npm의 이름이 `omo`인 다른 패키지를 설치하지 않는다. 실제 제품·에디션·버전이 다르면 명령·설정·지침 로딩부터 해당 경로로 확인한다. [공식 README](https://github.com/code-yeongyu/oh-my-openagent), [공식 문서](https://omo.dev/docs)

## 시작·설치·지침 연결

1. [README](../README.md)와 [AGENTS.md](../AGENTS.md)를 명시적으로 읽게 하고, [초기 셋업](<../10_구축/초기 셋업 흐름.md>)에서 구축 도구와 운영 실행기를 따로 정한다. 자동 발견만 믿고 필요한 운영 지침이 빠지지 않게 한다.
2. 설치된 실행 파일·패키지·버전을 확인한다. 미설치이면 대상 OS·배포 경로·고정 버전·설치 변경 범위와 복귀 방법을 정한 뒤 공식 경로로 설치한다. 공식 Native 패키지 후보는 `omo-ai`이고 `oh-my-openagent run`은 기존 OpenCode 실행 경로이므로 그대로 바꿔 쓰지 않는다.
3. 실제 Native 도움말에서 비대화형 호출·출력 형식·세션 지정·시간/권한 제어를 확인한다. 현재 공식 Native launcher는 Senpi를 사용하고 Senpi 문서는 print/JSON/RPC 모드를 제공하지만, 이를 **해당 설치 버전의 OmO가 같은 옵션으로 지원하는지** 실제 도움말과 작은 실행으로 검증한다. [Native 패키지](https://github.com/code-yeongyu/oh-my-openagent/blob/9e4443c92474fc99b1b7ce32d14f55882daf7c73/packages/omo-native/package.json), [Senpi 실행 모드](https://github.com/code-yeongyu/senpi/blob/main/packages/coding-agent/README.md)
4. 기존 인증·프로젝트 설정·스킬을 조사하고 필요한 것만 연결한다. `omo setup` 같은 이관 작업은 기존 키·설정·도구를 바꿀 수 있으므로 변경 내용과 백업을 확인한다. 이 문서를 읽었다는 이유로 이관·전체 권한 설정을 바로 실행하지 않는다.
5. 공식 현재 구성은 개인 `~/.omo/omo.jsonc`, 프로젝트 `.omo/omo.jsonc`를 안내한다. 설치 버전의 실제 경로·우선순위·로드 결과를 기록한다. legacy `opencode.json`이나 Codex 설정을 Native 설정으로 복사하지 않는다. [현재 설정 안내](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/reference/configuration.md)

## 능동 운영으로 연결

`ultrawork`·계획/검증·세션 재개는 진행 중 업무를 끝까지 수행하는 데 활용할 수 있다. 하지만 이것을 **내일 아침 새 작업을 깨우는 상시 스케줄러**로 간주하지 않는다. 확인한 공식 문서만으로 Native에 모든 정기 관찰·알림 기능이 기본 설치된다고 판정하지 않는다.

- [능동 운영과 완료 추적](<../10_구축/능동 운영과 완료 추적.md>)의 관찰·수정·검증·재점검 조건을 작업 지침으로 연결한다. 사용자 생활/기업 목표를 코드 작업 완료와 동일하게 판단하지 않는다.
- 확인된 Native 비대화형/RPC 호출을 외부 스케줄러에 연결하는 경우 [실행기 독립 운영 검증](<실행기 독립 운영 검증.md>) 3절의 상태·담당·한도·발신 어댑터를 함께 설정한다. 세션 지속 기능은 기존 것을 쓰고 업무 정본과 `taskId`로 연결한다.
- 현재 버전에서 무인 모드가 프로젝트 지침·확장·도구를 로드하는지 확인한다. 대화형 승인 창만 가능한 행동은 무인 흐름에서 대기/인계하고, 이를 해결하려고 광범위 권한으로 자동 변경하지 않는다.
- 세션 목표 반복과 시간 기반 재점검을 함께 쓸 때 어느 쪽이 작업을 소유하는지 정한다. 종료 조건·최대 실행 시간·모델 비용·자식 작업 정착을 바깥 실행기에서도 감시한다. `/goal` 등 명칭이나 옛 반복 횟수 설정이 실제 한도를 강제한다고 가정하지 않는다.
- 알림은 검증된 결과를 정한 발신 어댑터로 전달한다. 터미널 출력이나 모델의 “완료” 문장을 전달·업무 완료 증거로 대신하지 않는다. 호스트 OFF 동안 Native 프로세스와 외부 스케줄러도 실행되지 않는다.

Native 호출이 확인되지 않으면 자동 운영을 후보/미검증으로 남기고 정확한 남은 절차를 안내한다. 제품을 몰래 다른 edition으로 바꾸지 않는다. 사용자가 해당 대안을 선택하면 OpenCode edition의 공식 `oh-my-openagent run` 경로 또는 Codex edition의 호스트 기능을 별도 구성으로 검증한다. [edition별 CLI 구분](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/reference/cli.md)

## 동일 수용시험과 현재 증거

[P01–P06](<실행기 독립 운영 검증.md>)을 선택한 Native 경로 전체에 적용한다. P01은 원 대화를 닫은 다음 회차가 시작되는지, P03/P04는 불완전 작업의 `taskId`·외부 결과·담당을 유지하는지, P06은 중지·권한 회수와 완료 근거가 작동하는지 확인한다. 실행기 교체 시 기존 상태와 이전 프로세스 소유권을 대조한다.

- 문서/소스: 공식 사이트와 저장소, Native/기존 edition 분리, 공개 소스 기준 `9e4443c92474fc99b1b7ce32d14f55882daf7c73` 확인.
- 로컬 도움말: 이번 환경에는 `omo`·`opencode`가 없어 실행하지 못했다.
- 실제 모델·예약·인증·알림·운영: 미수행. 제품 설치나 `ultrawork` 성공을 이번 문서의 검증 결과로 주장하지 않는다.
