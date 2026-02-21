/* Analysis Page Interactivity - Simplified Modern */
document.addEventListener("DOMContentLoaded", () => {
    // 1. HEALTH GAUGE ANIMATION
    const progressCircle = document.getElementById('gauge-progress');
    if (progressCircle) {
        const score = parseInt(progressCircle.dataset.score) || 0;
        const circumference = 2 * Math.PI * 42;
        const offset = circumference - (score / 100) * circumference;

        // Target colors
        const color = score > 50 ? '#16C47F' : (score > 30 ? '#FF9D23' : '#F93827');

        setTimeout(() => {
            progressCircle.style.strokeDashoffset = offset;
            progressCircle.style.stroke = color;

            // Background for center
            const gaugeCenter = document.getElementById('gauge-center-bg');
            if (gaugeCenter) gaugeCenter.style.backgroundColor = color;

            // Verdict tag color
            const verdictBadge = document.getElementById('verdict-badge');
            if (verdictBadge) verdictBadge.style.backgroundColor = color;
        }, 300);
    }

    // 2. NUTRIENT BARS ANIMATION
    const nutrientBars = document.querySelectorAll('.progress-bar-custom');
    nutrientBars.forEach(bar => {
        const targetWidth = bar.style.getPropertyValue('--target-width');
        const delay = parseInt(bar.dataset.delay) || 0;

        setTimeout(() => {
            bar.style.width = targetWidth;
        }, 500 + delay);
    });

    // 3. ACCORDION AUTO-SCROLL
    const accordionItems = document.querySelectorAll('.accordion-collapse');
    accordionItems.forEach(item => {
        item.addEventListener('shown.bs.collapse', () => {
            item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        });
    });
});
