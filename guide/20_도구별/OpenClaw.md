---
type: guide
description: Current OpenClaw automation setup, heartbeat migration and runtime-independent verification with explicit host and state boundaries.
author:
  - Codex
date created: 2026-10-28
date modified: 2026-10-28
status: reference-verified-runtime-unverified
aliases:
  - 가재 에이전트
tags:
  - ai-agent
  - build-package
---

# OpenClaw를 사용할 경우

사용자가 말한 ‘가재’는 **OpenClaw**를 뜻한다고 가정한다. 실제 설치 제품·패키지·버전과 운영 호스트를 확인한 다음 [README](../README.md)·[AGENTS.md](../AGENTS.md) 및 [초기 셋업](<../10_구축/초기 셋업 흐름.md>)에서 시작한다. 구축에 쓰는 도구와 OpenClaw 운영 실행기를 따로 기록한다.

## 현재 예약 구조와 기존 heartbeat의 차이

2026-10-28 공식 문서는 **Automations**가 주기·일회성·관찰 작업을 맡으며 `openclaw automations`로 관리한다고 안내한다. `openclaw cron`은 해당 명령의 별칭이다. 예전 heartbeat monitor는 일반 automation job으로 이관하는 구조다. `HEARTBEAT.md` 파일을 만들거나 마스터에 “능동적으로 일하라”고 쓰는 것만으로 새 예약이 생성됐다고 판단하지 않는다. [Automations](https://docs.openclaw.ai/automation/cron-jobs), [Heartbeat 이관](https://docs.openclaw.ai/gateway/heartbeat)

예전 대화에서 암묵적 후속 약속을 추출하던 inferred commitments 기능은 현행 문서에서 제거됐다고 명시한다. 새 후속 점검은 **명시적인 업무 상태·다음 점검 시각·예약**으로 저장한다. 옛 shared Tasks ledger/TaskFlow 설명을 현재 시스템에 그대로 적용하지 않는다. [현행 자동화 구조](https://docs.openclaw.ai/automation)

## 설치·설정 순서

1. 설치 버전과 `openclaw --help`, `openclaw automations --help`, 선택한 `agent` 하위 도움말을 확인한다. 이 문서를 작성한 환경에는 OpenClaw가 없으므로 해당 명령을 실행했다고 기록하지 않는다.
2. 기존 Gateway·상태 DB·작업 폴더·채널·인증·스케줄을 조사한다. 신규이면 공식 설치/온보딩으로 실제 OS·모델·실행 계정·비밀 저장·작업 폴더·서비스 감독을 정한다. Gateway 시작/중지·상태 확인과 재부팅 후 기동을 실제로 검증한다. [Gateway 서비스](https://docs.openclaw.ai/cli/gateway/service)
3. 이전 heartbeat 구성이 있으면 원본·상태를 백업하고 설치 버전에 맞는 이관 절차를 적용한다. 현행 `doctor --fix`는 **변경 작업**이다. 실행 전에 변환 대상·백업을 확인하고 이관 후 job 목록·기존 ID·중지 상태·이력을 대조한다. 이 문서 작업에서는 실행하지 않았다.
4. [능동 운영과 완료 추적](<../10_구축/능동 운영과 완료 추적.md>)에서 정한 관찰 대상·허용 수정·완료 기준·재점검·제안을 job prompt와 읽을 업무 정본에 연결한다. morning/noon/evening 등 선택한 주기·시간대·활동 시간과 이벤트 조건을 설정한다.
5. job ID, agent·실행 계정, main/isolated 등 선택한 실행 문맥, 도구·권한 제한, 시간/비용 한도, 결과 저장과 delivery 대상/조용한 결과 정책을 확정한다. 실제 목록·상세 조회로 저장값과 다음 회차를 확인한다. [예약 관리](https://docs.openclaw.ai/automation/cron-jobs/managing-jobs), [전달 설정](https://docs.openclaw.ai/automation/cron-jobs/delivery)
6. 원 대화를 닫은 뒤 실제 예약이 시작되는지 시험한다. manual Run 한 번과 자동 회차를 구분하고, 실행 기록·실제 변경·완료 근거·미완료 다음 점검·허용된 알림까지 확인한다.

## Gateway·CLI·상태 경계

- Gateway 예약은 Gateway 프로세스가 켜져 있어야 동작한다. 현행 문서는 예약 정의·상태·이력을 공유 SQLite 상태 DB에 보존한다고 안내한다. 재시작 후 예약이 남는 것과 중단된 외부 작업이 안전하게 재실행되는 것은 별도 검증이다. [실행·복구 모델](https://docs.openclaw.ai/automation/cron-jobs/how-it-works)
- `openclaw agent`는 Gateway 경로의 한 턴 실행에, 지원 버전의 `openclaw agent exec`는 Gateway 없이 실행하는 headless 경로에 사용할 수 있다. `agent exec`의 기본 상태는 임시일 수 있으므로 지속 운영에는 업무 정본과 유지할 세션 상태를 명시한다. `--state-dir`을 쓰는 경우 실제 지원·기존 디렉터리·단일 쓰기 소유권을 확인하고, 켜진 Gateway의 상태 DB를 다른 writer가 함께 사용하게 하지 않는다. [Agent CLI](https://docs.openclaw.ai/cli/agent)
- headless 기본 도구·실행 권한이 운영 목적에 맞는지 검토하고 설정을 고정한다. 지침에 쓰인 제한만으로 OS·서비스 권한이 강제된다고 간주하지 않는다. 처음에는 관찰 또는 정한 시험 변경부터 검증한다.
- CLI+외부 스케줄러를 택하면 호출 시간 초과·프로세스 정리·같은 업무의 중복 시작·결과 유실·알림을 [실행기 독립 운영 계약](<실행기 독립 운영 검증.md>)으로 보완한다. 내장 예약과 외부 예약을 중복 활성화하지 않는다.
- OFF·누락 회차는 제품의 catch-up 동작과 사용자 정책을 대조한다. 늦은 일정을 전부 즉시 실행하거나 오래된 발송 승인을 재사용하지 않는다. 업무에 필요한 원본·내부망이 꺼져 있으면 별도 클라우드 Gateway가 있어도 그 기능은 제한된다.

## 동일 수용시험과 운영 인계

[P01–P06](<실행기 독립 운영 검증.md>)을 적용한다. job 실행 성공은 업무 완료가 아니다. 실제 결과·근거·후속 점검과 전달 결과를 각각 기록한다. 중지·snooze·접근 회수 시 예약과 실행 중 작업에 어떤 영향이 생기는지 실제 버전에서 확인하고 사용자에게 안내한다. 다른 실행기로 교체하면 기존 `taskId`·상태·권한·담당 락과 외부 변경을 대조한다.

이번 확인은 공식 문서 읽기뿐이다. OpenClaw 설치·도움말 실행·이관·Gateway 시작·계정 연결·모델 호출·실제 알림·P 시험은 수행하지 않았다. 해당 증거가 없는 상태를 “가재로 능동 운영 검증 완료”로 표현하지 않는다.
