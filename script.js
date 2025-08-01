(function(){
    const modal = document.getElementById('booking-modal');
    const openBtn = document.getElementById('open-modal');
    const closeBtn = document.getElementById('close-modal');
    const calendarEl = document.getElementById('calendar');
    const timeSlotsEl = document.getElementById('time-slots');
    const filters = document.querySelectorAll('.filter-btn');
    const classSelect = document.getElementById('class-select');
    const infoSection = document.getElementById('class-info');
    const infoType = document.getElementById('info-type');
    const infoPrice = document.getElementById('info-price');
    const infoSchedule = document.getElementById('info-schedule');
    const infoTrainer = document.getElementById('info-trainer');
    const totalEl = document.getElementById('total');

    const DAYS = ['Dom.', 'Lun.', 'Mar.', 'Mié.', 'Jue.', 'Vie.', 'Sáb.'];

    const CLASS_TYPES = {
        privada: {name: 'Clase Privada', price: 20},
        prueba: {name: 'Clase de prueba gratuita', price: 0}
    };

    const DURATION_MINUTES = 40;
    const TRAINER = 'Carlos';

    let selectedDay = null;
    let selectedTime = null;

    const TIME_SLOTS = {
        morning: createSlots(6, 12),
        afternoon: createSlots(12, 18),
        night: createSlots(18, 22)
    };

    function createSlots(startHour, endHour) {
        const slots = [];
        for(let h=startHour; h<endHour; h++) {
            slots.push(`${formatTime(h)}:00`);
            slots.push(`${formatTime(h)}:30`);
        }
        return slots;
    }

    function formatTime(num){
        return num < 10 ? '0'+num : num;
    }

    function openModal(){
        modal.classList.remove('hidden');
    }

    function closeModal(){
        modal.classList.add('hidden');
    }

    function renderCalendar(){
        const today = new Date();
        calendarEl.innerHTML = '';
        for(let i=0;i<7;i++){
            const d = new Date(today);
            d.setDate(today.getDate()+i);
            const btn = document.createElement('button');
            btn.textContent = `${DAYS[d.getDay()]} ${d.getDate()}`;
            btn.addEventListener('click', ()=>selectDay(btn));
            calendarEl.appendChild(btn);
            if(i===0){
                selectDay(btn);
            }
        }
    }

    function selectDay(btn){
        calendarEl.querySelectorAll('button').forEach(b=>b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedDay = btn.textContent;
    }

    function renderTimeSlots(filter){
        timeSlotsEl.innerHTML='';
        TIME_SLOTS[filter].forEach(t=>{
            const b = document.createElement('button');
            b.textContent=t;
            b.addEventListener('click', ()=>selectTime(b,t));
            timeSlotsEl.appendChild(b);
        });
    }

    function selectTime(button,time){
        timeSlotsEl.querySelectorAll('button').forEach(b=>b.classList.remove('selected'));
        button.classList.add('selected');
        selectedTime = time;
        updateInfo();
    }

    function updateInfo(){
        if(!selectedTime) return;
        const type = classSelect.value;
        const data = CLASS_TYPES[type];
        infoType.textContent = data.name;
        infoPrice.textContent = `${data.price.toFixed(2)} €`;
        infoSchedule.textContent = `${selectedTime} - ${calculateEndTime(selectedTime)}`;
        infoTrainer.textContent = `Entrenador: ${TRAINER}`;
        totalEl.textContent = `${data.price.toFixed(2)} €`;
        infoSection.classList.remove('hidden');
    }

    function calculateEndTime(start){
        const [h,m] = start.split(':').map(Number);
        const startDate = new Date();
        startDate.setHours(h);
        startDate.setMinutes(m);
        startDate.setMinutes(startDate.getMinutes()+DURATION_MINUTES);
        const hh = formatTime(startDate.getHours());
        const mm = formatTime(startDate.getMinutes());
        return `${hh}:${mm}`;
    }

    openBtn.addEventListener('click', openModal);
    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', (e)=>{
        if(e.target === modal) closeModal();
    });

    filters.forEach(f=>{
        f.addEventListener('click', ()=>{
            filters.forEach(el=>el.classList.remove('active'));
            f.classList.add('active');
            renderTimeSlots(f.dataset.filter);
        });
    });

    renderCalendar();
    renderTimeSlots('morning');
})();
