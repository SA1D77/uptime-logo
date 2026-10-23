<template>
    <div class="header-clock">
        <span class="time">{{ time }}</span>
        <span class="date">{{ date }}</span>
    </div>
</template>

<script>
// Часы в шапке. Часовой пояс — из «Настройки → Общие», как у времени проверок.
export default {
    data() {
        return {
            now: new Date(),
            timer: null,
        };
    },

    computed: {
        timeZone() {
            return this.$root.timezone || undefined;
        },
        locale() {
            return this.$i18n?.locale || undefined;
        },
        time() {
            return this.format({ hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false });
        },
        date() {
            return this.format({ weekday: "short", day: "numeric", month: "short" });
        },
    },

    mounted() {
        this.timer = setInterval(() => {
            this.now = new Date();
        }, 1000);
    },

    beforeUnmount() {
        clearInterval(this.timer);
    },

    methods: {
        format(options) {
            try {
                return new Intl.DateTimeFormat(this.locale, { ...options, timeZone: this.timeZone }).format(this.now);
            } catch (e) {
                return new Intl.DateTimeFormat(undefined, options).format(this.now);
            }
        },
    },
};
</script>

<style lang="scss" scoped>
.header-clock {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-left: 20px;
    padding-left: 20px;
    border-left: 1px solid #dee2e6;
    line-height: 1.15;

    .time {
        font-size: 1.35rem;
        font-weight: 600;
        font-variant-numeric: tabular-nums;
        color: #343a40;
    }

    .date {
        font-size: 0.8rem;
        color: #6c757d;
    }

    .dark & {
        border-left-color: #2c3440;

        .time {
            color: #e1e5ea;
        }

        .date {
            color: #8b949e;
        }
    }
}
</style>
