import pytest
from rag_engine import RAGHRBot

# Test inisialisasi bot
@pytest.fixture
def bot():
    return RAGHRBot()

# Test fungsi get_answer dengan input pertanyaan
def test_get_answer(bot):
    question = "Apa itu HR?"
    answer = bot.get_answer(question)
    assert isinstance(answer, str)
    assert len(answer) > 0

# Test memory percakapan
def test_multi_turn_memory(bot):
    # Pertanyaan pertama
    question1 = "Apa itu HR?"
    answer1 = bot.get_answer(question1)
    
    # Pertanyaan kedua setelah percakapan pertama
    question2 = "Apa tugas HR?"
    answer2 = bot.get_answer(question2)

    # Pastikan kedua jawaban ada di memory percakapan
    assert "HR" in answer1
    assert "tugas" in answer2

# Test feedback
def test_feedback(bot):
    question = "Apa itu HR?"
    answer = "HR adalah Human Resources"
    feedback = "Bagus"
    
    response = bot.provide_feedback(question, answer, feedback)
    assert "Terima kasih atas feedback Anda!" in response

