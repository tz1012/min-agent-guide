---
type: guide
description: Local Codex entry and configuration guidance for the self-contained agent-system build package.
author:
  - Codex
date created: 2026-10-28
date modified: 2026-10-28
status: reference-verified-not-executed
aliases: []
tags:
  - ai-agent
  - build-package
---

# Codex를 사용할 경우

## 시작

이 폴더의 루트를 작업 디렉터리로 열고 [AGENTS.md](../AGENTS.md)와 [README](../README.md)를 읽도록 요청한다. 자동 지침 발견에 의존하지 않아도 명시적으로 문서를 읽어 구축을 진행할 수 있다. 사용 환경의 상위 지침·권한도 함께 적용된다.

## 개인 시스템

- 이 패키지의 `AGENTS.md`는 프로젝트 공통 원칙이다. 개인 전역 선호는 기본적으로 `~/.codex/AGENTS.md`에 두지만, 이 폴더를 읽기 위해 그 파일이 필요한 것은 아니다.
- Codex는 전역 지침과 저장소 루트부터 현재 작업 폴더까지의 지침을 조합한다. 가까운 폴더가 앞선 지침보다 우선하며, 같은 위치에서 `AGENTS.override.md`가 있으면 먼저 선택된다.
- 실제 반복 절차가 확정되면 프로젝트 `.agents/skills/<이름>/SKILL.md`에 배치할 수 있다. 개인 공통 스킬의 기본 위치는 `~/.agents/skills`다.
- 스킬 설명에는 사용 조건을 구체적으로 쓰고, 본문에는 핵심 절차·완료 확인을 둔다. 같은 이름의 스킬이 병합된다고 가정하지 않는다. 필요하면 이름을 구분하고 `/skills` 또는 `$` 선택으로 확인한다.

## 엔터프라이즈 시스템

- 조직·팀·개인의 수정 범위와 담당자를 먼저 정한다. 관리자 공용 스킬 위치의 예는 `/etc/codex/skills`이며, 팀 절차는 저장소에 배포할 수 있다.
- 필수 실행 제한은 지원되는 관리자 `requirements.toml`과 원본 서비스 권한으로 집행한다. `AGENTS.md`나 스킬 내용만으로 권한 제한을 강제할 수 있다고 가정하지 않는다.
- 관리자 요구사항, 변경 가능한 기본 설정, 워크스페이스 권한, 외부 서비스 권한을 구분한다. 로컬·클라우드·앱별 적용 범위는 동일하지 않을 수 있다.

## 구축·확인

1. [결정·규칙 양식](<../30_양식/구축 결정·규칙 기록.md>)에서 구축 도구와 실제 운영 실행기를 별도로 기록한다.
2. [초기 셋업 흐름](<../10_구축/초기 셋업 흐름.md>)으로 환경 확인·단계별 결정·설치·재개를 진행하고, 해당 단계에서 [공통 구축 절차](<../10_구축/구축·운영 절차.md>)를 읽는다. 이 폴더에 작업별 스킬이 이미 설치되어 있다고 가정하지 않는다.
3. 현재 버전·실제로 읽은 지침 경로·선택한 스킬·권한 설정을 기록하고 정상/거부 동작을 확인한다.
4. 큰 마스터 문서를 만드는 대신 작업 조건에 따라 상세 문서를 읽는다. 원문 자료는 자동 적용 지침으로 로드하지 않는다.

## 확인 근거

2026-10-28 공식 문서 확인. 현 로컬 CLI 버전 확인 기록은 0.162.1이지만 이 안내대로 시스템을 설치·검증한 것은 아니다.

- [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Skills](https://learn.chatgpt.com/docs/build-skills)
- [관리형 설정](https://learn.chatgpt.com/docs/enterprise/managed-configuration)

필요한 절차는 이 안내와 공통 문서에 수록했다. 링크는 확인 출처이며 폴더의 필수 문서 위치가 아니다.
