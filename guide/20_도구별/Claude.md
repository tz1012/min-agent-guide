---
type: guide
description: Local Claude Code entry, instruction routing, and governance guidance for the self-contained build package.
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

# Claude를 사용할 경우

이 안내의 파일 기반 설정은 Claude Code 기준이다. 다른 Claude 환경에서는 폴더를 열거나 파일을 제공한 뒤 [README](../README.md)와 [AGENTS.md](../AGENTS.md)를 명시적으로 읽도록 요청한다.

## 시작과 개인 설정

- 패키지 루트의 `CLAUDE.md`는 짧은 공통 `AGENTS.md`를 가져온다. 가져오기나 자동 발견이 지원되지 않으면 두 파일을 직접 읽는다.
- 개인 전역 지침의 기본 위치는 `~/.claude/CLAUDE.md`, 프로젝트 지침은 프로젝트의 `CLAUDE.md`다. 개인 프로젝트 예외는 `CLAUDE.local.md`로 구분하고 공유 저장소에서 제외할 수 있다.
- 여러 `CLAUDE.md`는 문맥에 함께 들어간다. 스킬 이름 충돌 시의 선택 순위와 지침 문맥 결합을 혼동하지 않는다.
- 반복 절차가 확정되면 프로젝트 `.claude/skills/<이름>/SKILL.md`로 만들 수 있다. 개인 공통 스킬은 `~/.claude/skills`에 둔다.
- 동명 스킬은 기업 관리 → 개인 → 프로젝트 순으로 선택된다. 플러그인 스킬은 `/플러그인명:스킬명`처럼 구분되므로 팀 절차가 개인 스킬에 가려지지 않게 이름과 호출 방법을 정한다.

## 필요한 규칙만 읽기

- `@path`로 나눈 문서를 모두 가져오면 입력량이 줄지 않는다. 이 패키지에서는 짧은 공통 원칙만 가져오고 상세 절차는 작업에 맞게 읽는다.
- 작업별 절차는 스킬로, 특정 파일에만 적용하는 규칙은 `.claude/rules`의 `paths` 조건으로 분기할 수 있다. 조건 없는 규칙은 시작 시 로드된다.
- 호출된 스킬 본문은 이후 턴에도 남을 수 있으므로 본문과 긴 참조 자료를 구분한다. 적용 파일은 `/memory` 또는 `/context`에서 확인한다.

## 엔터프라이즈 설정

- 조직 지침·팀 절차·개인 선호의 변경 담당과 범위를 구분한다.
- 조직 공용 스킬 배포와 필수 정책 집행을 구분한다. 계정 기반 조직 배포는 제공 대상과 사용 여부를 확인하고, 그룹별 플러그인 제공은 해당 Enterprise 기능 범위에서 구성한다.
- 실행 제한은 관리형 설정과 연결 서비스 권한으로 집행한다. 로컬/클라우드 지원 범위, 실제 적용 정책과 변경 가능한 기본값을 기록한다.
- 원문에 있는 과거 특정 사용자의 승인 규칙이나 운영 환경을 현재 조직 정책으로 복사하지 않는다.

## 구축·확인

[초기 셋업 흐름](<../10_구축/초기 셋업 흐름.md>)으로 환경 확인부터 진행하고, 현재 단계에 필요한 값만 [결정·규칙 양식](<../30_양식/구축 결정·규칙 기록.md>)에 채운다. [공통 구축 절차](<../10_구축/구축·운영 절차.md>)의 해당 항목으로 현재 로드된 지침, 적용 스킬, 허용/거부 동작의 증거를 남긴다. 이 패키지는 Claude 설정이나 스킬을 이미 설치한 상태가 아니다.

## 확인 근거

2026-10-28 공식 문서 확인. 아래 링크는 출처이며 본 안내를 이해하기 위해 외부 볼트 파일이 필요한 것은 아니다.

- [지침과 조건부 로딩](https://code.claude.com/docs/en/memory)
- [스킬](https://code.claude.com/docs/en/skills)
- [설정](https://code.claude.com/docs/en/settings)
- [조직 스킬 배포](https://support.claude.com/en/articles/13119606-provision-and-manage-skills-for-your-organization)
