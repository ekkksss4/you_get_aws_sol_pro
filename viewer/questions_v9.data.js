const RESTORED_Q96 = {
  qNumber: 96,
  question: "솔루션 설계자는 새 Amazon S3 버킷에 저장될 객체에 대한 클라이언트 측 암호화 메커니즘을 구현해야 합니다. 솔루션 설계자는 이를 위해 AWS Key Management Service(AWS KMS)에 저장되는 CMK를 생성했습니다. 솔루션 설계자는 다음 IAM 정책을 생성하여 IAM 역할에 연결했습니다. 테스트 중에 솔루션 설계자는 S3 버킷에서 기존 테스트 객체를 성공적으로 가져올 수 있었습니다. 그러나 새 객체를 업로드하려고 하면 오류 메시지가 나타납니다. 작업이 금지되었다는 오류 메시지가 표시됩니다. 모든 요구 사항을 충족하기 위해 솔루션 설계자가 IAM 정책에 추가해야 하는 작업은 무엇입니까?",
  choices: [
    { label: "A", text: "kms:GenerateDataKey" },
    { label: "B", text: "kms:GetKeyPolicy" },
    { label: "C", text: "kms:GetPublicKey" },
    { label: "D", text: "kms:Sign" },
  ],
  answer: "A",
  answers: ["A"],
};

if (Array.isArray(window.DEFAULT_QUESTIONS) && !window.DEFAULT_QUESTIONS.some((item) => Number(item.qNumber) === 96)) {
  window.DEFAULT_QUESTIONS.splice(95, 0, RESTORED_Q96);
}