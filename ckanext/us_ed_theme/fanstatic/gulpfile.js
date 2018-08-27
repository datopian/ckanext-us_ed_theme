var gulp = require('gulp');
var less = require('gulp-less');
var cleanCSS = require('gulp-clean-css');
var autoprefixer = require('gulp-autoprefixer');
// var sourcemaps = require('gulp-sourcemaps'); - Uncomment when developing

// Rebuild CSS from LESS
gulp.task('less', function () {
  return gulp.src('less/custom.less')
  // .pipe(sourcemaps.init()) - Uncomment when developing
  .pipe(less())
  .pipe(cleanCSS({
    compatibility: 'ie8'
  }))
  .pipe(autoprefixer({
    browsers: [
      "last 5 versions",
      "ie >= 11"
    ]
  }))
  // .pipe(sourcemaps.write()) - Uncomment when developing
  .pipe(gulp.dest('css'));
});

// Watch for LESS file changes
gulp.task('watch', function () {
  gulp.watch(['less/**/*.less'], gulp.parallel('less'));
});

// The default Gulp.js task
gulp.task('default', gulp.parallel('less', 'watch'));
