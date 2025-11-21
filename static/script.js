document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('slideForm');
    const inputSection = document.getElementById('inputSection');
    const reviewSection = document.getElementById('reviewSection');
    const resultArea = document.getElementById('resultArea');
    const errorArea = document.getElementById('errorArea');
    const errorMessage = document.getElementById('errorMessage');

    const generateBtn = document.getElementById('generateBtn');
    const finalizeBtn = document.getElementById('finalizeBtn');
    const backBtn = document.getElementById('backBtn');
    const startOverBtn = document.getElementById('startOverBtn');
    const slidesContainer = document.getElementById('slidesContainer');
    const downloadLink = document.getElementById('downloadLink');

    let currentData = null;

    // Step 1: Generate Content
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        setLoading(generateBtn, true);
        hideError();

        const formData = new FormData(form);
        const requestData = {
            university: formData.get('university'),
            subject: formData.get('subject'),
            lecturer: formData.get('lecturer'),
            topic: formData.get('topic'),
            context: formData.get('context'),
            num_slides: parseInt(formData.get('num_slides'))
        };

        try {
            const response = await fetch('/generate_content', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) throw new Error('Failed to generate content');

            currentData = await response.json();
            renderReview(currentData);

            // Switch to review view
            inputSection.classList.add('hidden');
            reviewSection.classList.remove('hidden');
            reviewSection.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            showError(error.message);
        } finally {
            setLoading(generateBtn, false);
        }
    });

    // Step 2: Finalize & Download
    finalizeBtn.addEventListener('click', async () => {
        setLoading(finalizeBtn, true);
        hideError();

        // Collect edited data
        const updatedData = collectEditedData();

        try {
            const response = await fetch('/create_pptx', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data: updatedData })
            });

            if (!response.ok) throw new Error('Failed to create PowerPoint');

            const result = await response.json();

            downloadLink.href = result.download_url;

            // Switch to result view
            reviewSection.classList.add('hidden');
            resultArea.classList.remove('hidden');
            resultArea.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            showError(error.message);
        } finally {
            setLoading(finalizeBtn, false);
        }
    });

    // Navigation
    backBtn.addEventListener('click', () => {
        reviewSection.classList.add('hidden');
        inputSection.classList.remove('hidden');
    });

    startOverBtn.addEventListener('click', () => {
        resultArea.classList.add('hidden');
        inputSection.classList.remove('hidden');
        form.reset();
        currentData = null;
    });

    // Helpers
    function renderReview(data) {
        slidesContainer.innerHTML = '';

        data.slides.forEach((slide, index) => {
            const card = document.createElement('div');
            card.className = 'slide-card';

            const contentText = slide.content.join('\n');

            card.innerHTML = `
                <div class="slide-header">
                    <span class="slide-number">Slide ${index + 1}</span>
                </div>
                <div class="form-group">
                    <label>Title</label>
                    <input type="text" class="edit-title" value="${slide.title}">
                </div>
                <div class="form-group">
                    <label>Content (one bullet per line)</label>
                    <textarea class="edit-content slide-content-edit">${contentText}</textarea>
                </div>
                <div class="form-group">
                    <label>Speaker Notes</label>
                    <textarea class="edit-notes" rows="2">${slide.speaker_notes || ''}</textarea>
                </div>
                <div class="form-group">
                    <label>Image Search Keywords (Leave empty for no image)</label>
                    <input type="text" class="edit-image-prompt" value="${slide.image_search_query || slide.image_prompt || ''}">
                </div>
            `;
            slidesContainer.appendChild(card);
        });
    }

    function collectEditedData() {
        const newData = { ...currentData };
        const cards = slidesContainer.querySelectorAll('.slide-card');

        newData.slides = Array.from(cards).map(card => {
            const title = card.querySelector('.edit-title').value;
            const contentRaw = card.querySelector('.edit-content').value;
            const notes = card.querySelector('.edit-notes').value;
            const imagePrompt = card.querySelector('.edit-image-prompt').value;

            return {
                title: title,
                content: contentRaw.split('\n').filter(line => line.trim() !== ''),
                speaker_notes: notes,
                image_search_query: imagePrompt
            };
        });

        return newData;
    }

    function setLoading(btn, isLoading) {
        if (isLoading) {
            btn.classList.add('loading');
            btn.disabled = true;
        } else {
            btn.classList.remove('loading');
            btn.disabled = false;
        }
    }

    function showError(msg) {
        errorMessage.textContent = msg;
        errorArea.classList.remove('hidden');
    }

    function hideError() {
        errorArea.classList.add('hidden');
    }
});
