package br.com.vansact;


import android.support.test.espresso.ViewInteraction;
import android.support.test.rule.ActivityTestRule;
import android.support.test.runner.AndroidJUnit4;
import android.test.suitebuilder.annotation.LargeTest;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;

import static android.support.test.InstrumentationRegistry.getInstrumentation;
import static android.support.test.espresso.Espresso.onView;
import static android.support.test.espresso.Espresso.pressBack;
import static android.support.test.espresso.Espresso.openActionBarOverflowOrOptionsMenu;
import static android.support.test.espresso.contrib.RecyclerViewActions.actionOnItemAtPosition;
import static android.support.test.espresso.action.ViewActions.*;
import static android.support.test.espresso.assertion.ViewAssertions.*;
import static android.support.test.espresso.matcher.ViewMatchers.*;

import br.com.activity.R;

import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.hamcrest.TypeSafeMatcher;
import org.hamcrest.core.IsInstanceOf;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.is;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class AppTestMigrator_shoppingListTest11_2 {

    @Rule
    public ActivityTestRule<br.com.vansact.MainApp> mActivityTestRule = new ActivityTestRule<>(br.com.vansact.MainApp.class);

    @Test
    public void apptestmigrator_shoppinglisttest11_2() {
        openActionBarOverflowOrOptionsMenu(getInstrumentation().getTargetContext());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TableLayout")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.EditText")).perform(replaceText("list1"), closeSoftKeyboard());
        
        onView(withText("OK")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.ListView/android.widget.TableLayout")).perform(click());
        
        onView(withId(R.id.header_description_collumn)).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView[2]")).perform(click());
        
        openActionBarOverflowOrOptionsMenu(getInstrumentation().getTargetContext());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView")).perform(click());
        
        onView(withText("Yes")).perform(click());
        
        onView(withId(R.id.action_add)).perform(longClick());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView")).perform(click());
        
        openActionBarOverflowOrOptionsMenu(getInstrumentation().getTargetContext());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[2]/android.widget.RelativeLayout/android.widget.TextView")).perform(click());
        
        openActionBarOverflowOrOptionsMenu(getInstrumentation().getTargetContext());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[3]/android.widget.RelativeLayout/android.widget.TextView")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView")).perform(click());
        
        openActionBarOverflowOrOptionsMenu(getInstrumentation().getTargetContext());
        
        pressBack();
        
        openActionBarOverflowOrOptionsMenu(getInstrumentation().getTargetContext());
        
        pressBack();
        
        onView(withXPath("/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.TableLayout")).perform(click());
        
        onView(withXPath("/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.EditText")).perform(replaceText("item1"), closeSoftKeyboard());
        
        }

        private static Matcher<View> childAtPosition(
            final Matcher<View> parentMatcher, final int position) {

        return new TypeSafeMatcher<View>() {
            @Override
            public void describeTo(Description description) {
                description.appendText("Child at position " + position + " in parent ");
                parentMatcher.describeTo(description);
            }

            @Override
            public boolean matchesSafely(View view) {
                ViewParent parent = view.getParent();
                return parent instanceof ViewGroup && parentMatcher.matches(parent)
                        && view.equals(((ViewGroup)parent).getChildAt(position));
            }
        };
    }
    }
