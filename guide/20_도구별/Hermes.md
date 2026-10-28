---
type: guide
description: A portable guide for using Hermes to build this agent system, with local entry points and version-aware instruction and skill discovery.
author:
  - Codex
date created: 2026-10-28
date modified: 2026-10-28
status: reference-verified-runtime-unverified
collectionPurpose: "폴더 안의 지침과 자료만으로 개인 또는 엔터프라이즈 에이전트 시스템의 구축을 시작하고 운영 조건을 정한다."
source:
  - https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
  - https://hermes-agent.nousresearch.com/docs/user-guide/configuration
  - https://github.com/NousResearch/hermes-agent/blob/19949783b23864da1da2f631ebbbb4d1cf6f9239/agent/prompt_builder.py
aliases: []
tags:
  - ai-agent
  - build-package
---

# Hermes를 사용할 경우

이 문서는 Hermes를 **구축 작업을 수행하는 도구**로 사용할 때의 진입 안내다. 완성할 시스템의 **운영 런타임도 Hermes로 할지는 별도로 결정**한다. Hermes로 문서를 읽고 구축한다고 해서 운영 도구까지 확정되는 것은 아니다.

## 시작과 공통 절차

1. 전달받은 폴더의 루트를 작업 디렉터리로 연다. [README](../README.md)와 [공통 마스터 지침](../AGENTS.md)을 읽는다.
2. [기능 정의](<../최소한의 에이전트 시스템 구축 - 기능 정의.md>)의 최소 범위와 미정 사항을 확인한다.
3. [초기 셋업 흐름](<../10_구축/초기 셋업 흐름.md>)으로 환경 확인·단계별 질문·설치·재개를 진행하고, [구축·운영 절차](<../10_구축/구축·운영 절차.md>)의 해당 단계를 적용한다. 이미 답한 내용은 재사용하고 관련 질문을 1–3개씩 묻는다.
4. 현재 단계에 필요한 규칙과 자료만 추가로 읽는다. 외부 URL은 근거이며, 이 폴더의 절차를 이해하기 위한 필수 진입점으로 삼지 않는다.

자동 지침 발견이나 스킬 등록이 되지 않으면 다음 문구로 시작한다.

```text
이 폴더를 작업 루트로 사용해줘. README.md와 AGENTS.md를 직접 읽고,
기능 정의와 10_구축/구축·운영 절차.md에 따라 미정 사항을 확인해줘.
자동 등록되지 않은 작업 지침도 필요한 때 파일로 직접 읽어 적용해줘.
구축 도구와 운영 런타임을 구분하고, 실행·검증하지 않은 것은 완료로 기록하지 마.
```

## 지침 발견과 버전 확인

- 검증한 기준은 **2026-10-28의 공식 저장소 main 커밋 `19949783b23864da1da2f631ebbbb4d1cf6f9239`**다. 특정 설치 릴리스의 실행 결과는 아니므로, 적용할 Hermes 버전과 실제 로드된 지침을 기록한다.
- 해당 코드는 `.hermes.md`/`HERMES.md` → `AGENTS.md` 계열 → `CLAUDE.md` → Cursor 규칙 중 처음 발견한 유효 유형만 로드한다. 서로 다른 진입 파일에 필수 원칙을 분산하지 않는다.
	- Git 저장소에서는 `AGENTS.md`를 저장소 루트부터 현재 디렉터리까지 결합한다. 디렉터리별로 `AGENTS.override.md`, `AGENTS.md`, `agents.md` 중 첫 유효 파일을 선택한다.
	- Git 저장소 밖에서는 현재 디렉터리의 지침을 확인한다. 따라서 일반 폴더를 전달할 때는 루트에서 시작하는 절차를 유지한다.
	- 기존 `.hermes.md`가 선택되거나 시작 경로가 다르면 공통 `AGENTS.md`가 자동 적용되지 않을 수 있다. README의 명시적 읽기 절차로 누락을 확인한다.
- 일부 공식 참고 문서에는 이전의 발견 방식이 남아 있다. 설치 버전의 동작이 다르면 자동 상속에 기대지 않고 필요한 파일을 직접 읽는다. 짧은 공통 원칙과 작업별 참조 구조를 유지한다.

## 작업 지침을 스킬로 등록할 때

- 이 패키지는 파일 읽기만으로 구축 절차를 시작할 수 있다. 네이티브 스킬 등록은 필요할 때 선택한다.
- 공식 문서의 프로젝트 스킬은 가장 가까운 `.git` 루트의 `.hermes/skills/` 또는 `.agents/skills/`를 탐색하며, 프로젝트 신뢰 설정이 선행된다. 일반 폴더에 파일만 둔 상태를 자동 등록 완료로 표시하지 않는다.
- 등록을 선택하면 설치 버전의 지원 여부, 저장소 루트, 스킬 이름·설명·본문, 적용 범위를 확인한 다음 `hermes skills trust`에 해당하는 신뢰 절차를 사용자가 이해한 상태에서 수행한다. 이 문서 작성 과정에서는 실행하지 않았다.
- 목록에 나타나는지, 의도한 작업에서 본문을 읽는지 확인한다. 같은 이름의 다른 스킬과 충돌하면 고유 이름으로 구분하고 실제 선택 경로를 기록한다.
- 공유 스킬의 배포 위치와 수정 권한을 구분한다. 문서상의 규칙만으로 조직 정책이 강제된다고 간주하지 않는다.

## Hermes를 운영 런타임으로 선택하면

- 공통 절차에 모델·제공자, 실행 환경, 작업 디렉터리, 필요한 도구와 연결, 인증 참조, 실행 권한, 승인 조건, 비용·시간 한도, 상태 저장과 실패 복구 방법을 구체적으로 기록한다.
- 개인 시스템은 개인 계정의 접근 범위와 확인이 필요한 행동을 정한다. 엔터프라이즈 시스템은 사용자·실행 계정·승인자, 조직·팀·개인 자료 경계, 정책 강제 수단과 관리 책임을 추가한다.
- 메모리·스킬의 자동 변경, 예약 작업, 외부 메시지 발송은 각각 사용 여부와 조건을 정한다. 운영 자격증명은 별도로 주입하고 문서나 배포 자료에 실제 비밀값을 넣지 않는다.
- 첫 업무의 정상 실행, 권한 거부, 연결 실패, 중복 요청, 재시작·복구를 확인한다. 사용 버전·설정·명령·실제 결과를 남기고 미구현·미검증 항목을 구분한다.

## 근거와 확인 범위

- [공식 지침 발견 코드 — 검증한 커밋](https://github.com/NousResearch/hermes-agent/blob/19949783b23864da1da2f631ebbbb4d1cf6f9239/agent/prompt_builder.py): 프로젝트 지침 선택, Git 경계, 디렉터리별 발견 방식 확인.
- [공식 Skills 문서](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills#project-local-skills): 프로젝트 스킬 경로와 신뢰 조건 확인.
- [공식 Configuration 문서](https://hermes-agent.nousresearch.com/docs/user-guide/configuration): 작업 디렉터리와 설정 역할 확인.
- 문서·소스 읽기만 수행했다. Hermes 설치·인증·신뢰 설정·시스템 구축·실행 성능 검증은 수행하지 않았다.
