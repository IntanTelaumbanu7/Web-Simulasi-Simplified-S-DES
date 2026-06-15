function cleanBinary(input, max){ input.value = input.value.replace(/[^01]/g,'').slice(0,max); }
function renderBits(id, value, len){
  const target = document.getElementById(id); if(!target) return;
  target.innerHTML='';
  const chars = value.padEnd(len, '-').slice(0,len);
  for(const ch of chars){ const s=document.createElement('span'); s.textContent=ch; target.appendChild(s); }
}
const input = document.getElementById('input_data');
const key = document.getElementById('key');
function refresh(){ cleanBinary(input,8); cleanBinary(key,10); renderBits('input-preview', input.value, 8); renderBits('key-preview', key.value, 10); }
if(input && key){ input.addEventListener('input', refresh); key.addEventListener('input', refresh); refresh(); }
document.querySelectorAll('.mode-option input').forEach(radio=>{
  radio.addEventListener('change',()=>{
    document.querySelectorAll('.mode-option').forEach(label=>label.classList.remove('active'));
    radio.closest('.mode-option').classList.add('active');
  });
});
const toggle = document.getElementById('toggle-solution');
const box = document.getElementById('solution-box');
if(toggle && box){ toggle.addEventListener('click',()=>{ const open = box.style.display !== 'none'; box.style.display = open ? 'none':'block'; toggle.textContent = open ? '▼ Tampilkan Solusi Penyelesaian' : '▲ Sembunyikan Solusi Penyelesaian'; }); }
